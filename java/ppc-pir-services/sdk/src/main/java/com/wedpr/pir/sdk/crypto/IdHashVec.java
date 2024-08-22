package com.wedpr.pir.sdk.crypto;

import com.wedpr.pir.sdk.exception.WedprException;
import com.wedpr.pir.sdk.exception.WedprStatusEnum;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

/**
 * @author zachma
 * @date 2024/8/20
 */
public class IdHashVec {
    public static List<String> getIdHashVec(int obfuscationOrder, Integer idIndex, String searchId)
            throws WedprException {

        List<String> clientDataBodyList = new ArrayList<>();
        String searchIdTemp;
        for (int i = 0; i < obfuscationOrder + 1; i++) {
            if (idIndex == i) {
                searchIdTemp = searchId;
            } else {
                String uuid = UUID.randomUUID().toString();
                searchIdTemp = makeHash(uuid.getBytes());
            }
            clientDataBodyList.add(searchIdTemp);
        }
        return clientDataBodyList;
    }

    private static String makeHash(byte[] data) throws WedprException {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hashBytes = digest.digest(data);

            StringBuilder hexString = new StringBuilder();
            for (byte b : hashBytes) {
                String hex = Integer.toHexString(0xFF & b);
                if (hex.length() == 1) {
                    hexString.append('0');
                }
                hexString.append(hex);
            }
            return hexString.toString();
        } catch (NoSuchAlgorithmException e) {
            throw new WedprException(WedprStatusEnum.WRONG_HASH_ERROR);
        }
    }
}
