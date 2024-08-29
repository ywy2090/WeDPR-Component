package com.wedpr.pir.sdk.exception;

/**
 * @author zachma
 * @date 2024/8/18
 */
public class WedprException extends Exception {
    private final WedprStatusEnum status;

    public WedprException(WedprStatusEnum status) {
        super(status.getMessage());
        this.status = status;
    }

    public WedprException(WedprStatusEnum status, String message) {
        super(message);
        this.status = status;
    }

    public WedprStatusEnum getStatus() {
        return status;
    }
}
