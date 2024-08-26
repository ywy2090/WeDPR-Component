package com.wedpr.pir.sdk.entity.response;

import com.wedpr.pir.sdk.entity.body.ServerResultList;
import java.util.List;
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
public class ServerOTResponse {
    List<ServerResultList> resultBodyList;
}
