package com.wedpr.pir.sdk.entity.response;

import com.wedpr.pir.sdk.entity.body.PirDataBody;
import java.math.BigInteger;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Data;

/**
 * @author zachma
 * @date 2024/8/20
 */
@Data
@AllArgsConstructor
public class ClientOTResponse {
    BigInteger b;
    BigInteger x;
    BigInteger y;
    List<PirDataBody> dataBodyList;
}
