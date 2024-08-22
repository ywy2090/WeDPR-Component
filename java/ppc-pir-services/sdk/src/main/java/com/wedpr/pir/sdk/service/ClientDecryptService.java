package com.wedpr.pir.sdk.service;

import com.sun.org.slf4j.internal.Logger;
import com.sun.org.slf4j.internal.LoggerFactory;
import com.wedpr.pir.sdk.entity.body.PirResultBody;
import com.wedpr.pir.sdk.entity.body.ServerResultBody;
import com.wedpr.pir.sdk.entity.request.ClientDecryptRequest;
import com.wedpr.pir.sdk.entity.response.ClientDecryptResponse;
import com.wedpr.pir.sdk.exception.WedprException;
import com.wedpr.pir.sdk.helper.AESHelper;
import com.wedpr.pir.sdk.helper.BasicTypeHelper;
import com.wedpr.pir.sdk.helper.ConvertTypeHelper;
import com.wedpr.pir.sdk.helper.CryptoOperatorHelper;
import java.math.BigInteger;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

/**
 * @author zachma
 * @date 2024/8/21
 */
public class ClientDecryptService {
    private static final Logger logger = LoggerFactory.getLogger(ClientDecryptService.class);
    private void decryptServerResultList(
            PirResultBody pirResultBody, List<ServerResultBody> serverResultList, BigInteger b) {
        for (ServerResultBody body : serverResultList) {
            BigInteger e = body.getE();
            BigInteger w = body.getW();
            String cipherStr = body.getC();
            BigInteger w1 = CryptoOperatorHelper.OTPow(w, b);
            try {
                // 对整数AES密钥OT解密，报错后不处理
                BigInteger messageRecover = w1.xor(e);
                byte[] convertedBytes = ConvertTypeHelper.bigIntegerToBytes(messageRecover);
                String convertedStr = new String(convertedBytes, StandardCharsets.UTF_8);
                String decryptedText = AESHelper.decrypt(cipherStr, convertedStr);
                pirResultBody.setSearchValue(decryptedText);
            } catch (WedprException ignored) {

            }
        }
    }

    protected ClientDecryptResponse runDecryptOTparam(ClientDecryptRequest clientDecryptRequest) {
        logger.debug("runDecryptOTparam Start: ", clientDecryptRequest);
        List<PirResultBody> pirResultBodyArrayList = new ArrayList<>();
        for (int i = 0;
                i < clientDecryptRequest.getServerResult().getResultBodyList().size();
                i++) {
            PirResultBody pirResultBody = new PirResultBody();
            pirResultBody.setSearchId(clientDecryptRequest.getDataBodyList().get(i));
            List<ServerResultBody> serverResultlist =
                    clientDecryptRequest
                            .getServerResult()
                            .getResultBodyList()
                            .get(i)
                            .getResultBodyList();
            decryptServerResultList(pirResultBody, serverResultlist, clientDecryptRequest.getB());
            pirResultBody.setSearchExist(
                    BasicTypeHelper.isStringNotEmpty(pirResultBody.getSearchValue()));
            pirResultBodyArrayList.add(pirResultBody);
        }
        logger.debug("runDecryptOTparam Success: ", pirResultBodyArrayList);
        ClientDecryptResponse clientDecryptResponse = new ClientDecryptResponse();
        clientDecryptResponse.setDetail(pirResultBodyArrayList);
        return clientDecryptResponse;
    }
}
