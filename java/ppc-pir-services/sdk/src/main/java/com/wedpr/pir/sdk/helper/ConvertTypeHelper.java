package com.wedpr.pir.sdk.helper;

import java.math.BigInteger;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;

/**
 * @author zachma
 * @date 2024/8/19
 */
public class ConvertTypeHelper {
    public static int bytesToInt(byte[] bytes, ByteOrder byteOrder) {
        ByteBuffer buffer = ByteBuffer.wrap(bytes).order(byteOrder);
        return buffer.getInt();
    }

    public static byte[] intToBytes(int number, ByteOrder byteOrder) {
        ByteBuffer buffer = ByteBuffer.allocate(Integer.BYTES).order(byteOrder);
        buffer.putInt(number);
        return buffer.array();
    }

    public static BigInteger bytesToBigInteger(byte[] bytes) {
        return new BigInteger(1, bytes);
    }

    public static byte[] bigIntegerToBytes(BigInteger number) {
        byte[] bytes = number.toByteArray();
        if (bytes[0] == 0) {
            byte[] tmpBytes = new byte[bytes.length - 1];
            System.arraycopy(bytes, 1, tmpBytes, 0, tmpBytes.length);
            return tmpBytes;
        }
        return bytes;
    }

    public static String bytesToHexString(byte[] bytes) {
        StringBuilder sb = new StringBuilder();
        for (byte b : bytes) {
            sb.append(String.format("%02X ", b));
        }
        return sb.toString().trim();
    }
}
