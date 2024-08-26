package com.wedpr.pir.sdk.entity.body;

import com.wedpr.pir.sdk.entity.response.ServerOTResponse;
import lombok.Data;

/**
 * @author zachma
 * @date 2024/8/21
 */
@Data
public class SimpleEntity {
    String code;
    String message;
    ServerOTResponse data;
}
