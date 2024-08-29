package com.wedpr.pir.sdk.entity.request;

import java.util.List;
import lombok.Data;

/**
 * @author zachma
 * @date 2024/8/20
 */
@Data
public class ClientOTRequest {
    int filterLength = 4;

    int obfuscationOrder;

    List<String> dataBodyList;
}
