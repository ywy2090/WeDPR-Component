package com.wedpr.pir.sdk.helper;

/**
 * @author zachma
 * @date 2024/8/21
 */
public class BasicTypeHelper {
    public static boolean isStringEmpty(String str) {
        return str == null || str.length() == 0;
    }

    public static boolean isStringNotEmpty(String str) {
        return !isStringEmpty(str);
    }
}
