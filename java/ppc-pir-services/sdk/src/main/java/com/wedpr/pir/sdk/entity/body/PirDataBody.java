package com.wedpr.pir.sdk.entity.body;

import java.math.BigInteger;
import java.util.List;
import lombok.Data;

/**
 * @author zachma
 * @date 2024/8/18
 */
@Data
public class PirDataBody {
    BigInteger z0;
    String filter;
    int idIndex;
    List<String> idHashList;
}
