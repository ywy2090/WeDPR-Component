package com.wedpr.pir.sdk.helper;

import com.wedpr.pir.sdk.exception.WedprException;
import com.wedpr.pir.sdk.exception.WedprStatusEnum;
import java.nio.charset.StandardCharsets;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.util.Base64;
import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.SecretKeySpec;

/**
 * @author zachma
 * @date 2024/8/21
 */
public class AESHelper {
    private static final SecureRandom SECURE_RANDOM = new SecureRandom();

    private static final String AES_ALGORITHM_TRANSFORMATION = "AES/GCM/NoPadding";

    public static String generateRandomKey() {
        // 随机生成 16 位字符串格式的密钥
        byte[] keyBytes = new byte[16];
        SECURE_RANDOM.nextBytes(keyBytes);
        return Base64.getEncoder().encodeToString(keyBytes);
    }

    public static String encrypt(String plainText, String keyString) throws WedprException {
        try {
            byte[] iv = new byte[12];
            SecureRandom secureRandom = new SecureRandom();
            secureRandom.nextBytes(iv);
            byte[] contentBytes = plainText.getBytes(StandardCharsets.UTF_8);
            Cipher cipher = Cipher.getInstance(AES_ALGORITHM_TRANSFORMATION);
            GCMParameterSpec params = new GCMParameterSpec(128, iv);
            cipher.init(Cipher.ENCRYPT_MODE, getSecretKey(keyString), params);
            byte[] encryptData = cipher.doFinal(contentBytes);
            assert encryptData.length == contentBytes.length + 16;
            byte[] message = new byte[12 + contentBytes.length + 16];
            System.arraycopy(iv, 0, message, 0, 12);
            System.arraycopy(encryptData, 0, message, 12, encryptData.length);
            return Base64.getEncoder().encodeToString(message);
        } catch (Exception e) {
            throw new WedprException(WedprStatusEnum.AES_ENCRYPT_ERROR);
        }
    }

    public static String decrypt(String encryptedText, String keyString) throws WedprException {
        try {
            byte[] content = Base64.getDecoder().decode(encryptedText);
            if (content.length < 12 + 16) {
                throw new IllegalArgumentException();
            }
            GCMParameterSpec params = new GCMParameterSpec(128, content, 0, 12);
            Cipher cipher = Cipher.getInstance(AES_ALGORITHM_TRANSFORMATION);
            cipher.init(Cipher.DECRYPT_MODE, getSecretKey(keyString), params);
            byte[] decryptData = cipher.doFinal(content, 12, content.length - 12);
            return new String(decryptData, StandardCharsets.UTF_8);
        } catch (Exception e) {
            throw new WedprException(WedprStatusEnum.AES_DECRYPT_ERROR);
        }
    }

    private static SecretKeySpec getSecretKey(String key) throws NoSuchAlgorithmException {
        KeyGenerator kg = KeyGenerator.getInstance("AES");
        // 初始化密钥生成器，AES要求密钥长度为128位、192位、256位
        SecureRandom secureRandom = SecureRandom.getInstance("SHA1PRNG");
        secureRandom.setSeed(key.getBytes(StandardCharsets.UTF_8));
        kg.init(128, secureRandom);
        SecretKey secretKey = kg.generateKey();
        return new SecretKeySpec(secretKey.getEncoded(), "AES");
    }
}
