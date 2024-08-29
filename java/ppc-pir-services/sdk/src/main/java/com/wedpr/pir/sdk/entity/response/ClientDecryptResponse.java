package com.wedpr.pir.sdk.entity.response;

import com.wedpr.pir.sdk.entity.body.PirResultBody;
import java.util.List;
import lombok.Data;

/**
 * @author zachma
 * @date 2024/8/21
 */
@Data
public class ClientDecryptResponse {
    List<PirResultBody> detail;
}
