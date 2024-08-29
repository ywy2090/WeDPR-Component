package com.wedpr.pir.sdk.entity.body;

import lombok.Data;

/**
 * @author zachma
 * @date 2024/8/21
 */
@Data
public class PirResultBody {
    String searchId;
    Boolean searchExist;
    String searchValue;
}
