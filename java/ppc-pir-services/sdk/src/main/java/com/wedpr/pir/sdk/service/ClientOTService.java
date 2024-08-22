package com.wedpr.pir.sdk.service;

import com.sun.org.slf4j.internal.Logger;
import com.sun.org.slf4j.internal.LoggerFactory;
import com.wedpr.pir.sdk.crypto.IdHashVec;
import com.wedpr.pir.sdk.entity.body.PirDataBody;
import com.wedpr.pir.sdk.entity.request.ClientOTRequest;
import com.wedpr.pir.sdk.entity.response.ClientOTResponse;
import com.wedpr.pir.sdk.exception.WedprException;
import com.wedpr.pir.sdk.helper.ConvertTypeHelper;
import com.wedpr.pir.sdk.helper.CryptoOperatorHelper;
import java.math.BigInteger;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/**
 * @author zachma
 * @date 2024/8/20
 */
public class ClientOTService {
    private static final Logger logger = LoggerFactory.getLogger(ClientOTService.class);
    private final Random rand = new Random();

    /* hash披露, 请求方选择id，生成随机数a、b */
    protected ClientOTResponse runClientOTParam(ClientOTRequest clientOTRequest) {
        logger.debug("runClientOTParam start: ", clientOTRequest);
        int filterLength = clientOTRequest.getFilterLength();
        BigInteger blindingA = CryptoOperatorHelper.getRandomInt();
        BigInteger blindingB = CryptoOperatorHelper.getRandomInt();

        BigInteger x = CryptoOperatorHelper.powMod(blindingA);
        BigInteger y = CryptoOperatorHelper.powMod(blindingB);
        BigInteger blindingC = CryptoOperatorHelper.mulMod(blindingA, blindingB);

        List<PirDataBody> pirDataArrayList = new ArrayList<>();
        for (String searchId : clientOTRequest.getDataBodyList()) {
            String filter =
                    searchId.length() < filterLength
                            ? searchId
                            : searchId.substring(0, filterLength);
            BigInteger z0 = calculateZ0(searchId, blindingC);
            PirDataBody pirDataBody = new PirDataBody();
            pirDataBody.setFilter(filter);
            pirDataBody.setZ0(z0);
            pirDataArrayList.add(pirDataBody);
        }
        logger.debug("runClientOTParam success: ", pirDataArrayList);
        return new ClientOTResponse(blindingB, x, y, pirDataArrayList);
    }

    /* hash筛选, 请求方选择顺序\delta\in \{0,1,..,m-1\}，生成随机数a、b */
    protected ClientOTResponse runClientOTCipher(ClientOTRequest clientOTRequest)
            throws WedprException {
        logger.debug("runClientOTCipher start: ", clientOTRequest);

        int obfuscationOrder = clientOTRequest.getObfuscationOrder();
        BigInteger blindingA = CryptoOperatorHelper.getRandomInt();
        BigInteger blindingB = CryptoOperatorHelper.getRandomInt();

        BigInteger x = CryptoOperatorHelper.powMod(blindingA);
        BigInteger y = CryptoOperatorHelper.powMod(blindingB);
        BigInteger blindingC = CryptoOperatorHelper.mulMod(blindingA, blindingB);

        List<PirDataBody> pirDataArrayList = new ArrayList<>();
        for (String searchId : clientOTRequest.getDataBodyList()) {
            int idIndex = rand.nextInt(obfuscationOrder + 1);
            BigInteger z0 = calculateIndexZ0(idIndex, blindingC);
            List<String> idHashVecList =
                    IdHashVec.getIdHashVec(obfuscationOrder, idIndex, searchId);

            PirDataBody pirDataBody = new PirDataBody();
            pirDataBody.setZ0(z0);
            pirDataBody.setIdIndex(idIndex);
            pirDataBody.setIdHashList(idHashVecList);
            pirDataArrayList.add(pirDataBody);
        }
        logger.debug("runClientOTCipher success: ", pirDataArrayList);
        return new ClientOTResponse(blindingB, x, y, pirDataArrayList);
    }

    private BigInteger calculateZ0(String searchId, BigInteger blindingC) {
        byte[] idBytes = searchId.getBytes(StandardCharsets.UTF_8);
        BigInteger idNumber = ConvertTypeHelper.bytesToBigInteger(idBytes);
        return CryptoOperatorHelper.powMod(blindingC.subtract(idNumber));
    }

    private BigInteger calculateIndexZ0(Integer idIndex, BigInteger blindingC) {
        // 将整数转长整数
        BigInteger idNumber = BigInteger.valueOf(idIndex);
        return CryptoOperatorHelper.powMod(blindingC.subtract(idNumber));
    }
}
