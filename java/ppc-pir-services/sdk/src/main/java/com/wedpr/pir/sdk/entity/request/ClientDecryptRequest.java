package com.wedpr.pir.sdk.entity.request;

import com.wedpr.pir.sdk.entity.response.ServerOTResponse;
import java.math.BigInteger;
import java.util.List;
import lombok.Data;

/**
 * @author zachma
 * @date 2024/8/21
 */
@Data
public class ClientDecryptRequest {
    BigInteger b;
    List<String> dataBodyList;
    ServerOTResponse serverResult;
}
