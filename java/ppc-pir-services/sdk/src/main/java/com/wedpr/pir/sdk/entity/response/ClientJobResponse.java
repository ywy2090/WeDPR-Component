package com.wedpr.pir.sdk.entity.response;

import com.wedpr.pir.sdk.exception.WedprStatusEnum;
import lombok.Data;

/**
 * @author zachma
 * @date 2024/8/18
 */
@Data
public class ClientJobResponse {
    private String code;
    private String message;
    private Object data;

    public ClientJobResponse(WedprStatusEnum wedprStatusEnum) {
        this.code = wedprStatusEnum.getCode();
        this.message = wedprStatusEnum.getMessage();
    }

    public ClientJobResponse(WedprStatusEnum wedprStatusEnum, Object data) {
        this.code = wedprStatusEnum.getCode();
        this.message = wedprStatusEnum.getMessage();
        this.data = data;
    }
}
