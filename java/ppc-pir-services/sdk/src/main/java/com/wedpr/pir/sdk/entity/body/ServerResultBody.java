package com.wedpr.pir.sdk.entity.body;

import java.math.BigInteger;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * @author zachma
 * @date 2024/8/18
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
public class ServerResultBody {
    BigInteger e;
    BigInteger w;
    String c;
}
