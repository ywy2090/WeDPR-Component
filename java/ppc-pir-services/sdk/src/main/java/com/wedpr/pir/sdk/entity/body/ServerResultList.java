package com.wedpr.pir.sdk.entity.body;

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
public class ServerResultList {
    List<ServerResultBody> resultBodyList;
}
