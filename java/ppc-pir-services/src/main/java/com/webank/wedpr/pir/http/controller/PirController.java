package com.webank.wedpr.pir.http.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.webank.wedpr.pir.http.common.Constant;
import com.webank.wedpr.pir.http.service.PirAppService;
import com.wedpr.pir.sdk.entity.request.ServerJobRequest;
import com.wedpr.pir.sdk.entity.response.ClientJobResponse;
import com.wedpr.pir.sdk.entity.response.ServerOTResponse;
import com.wedpr.pir.sdk.exception.WedprStatusEnum;
import lombok.extern.slf4j.Slf4j;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

/**
 * @author zachma
 * @date 2024/8/18
 */
@RestController
@Slf4j
public class PirController {
    private static final Logger logger = LoggerFactory.getLogger(PirController.class);

    @Autowired private ObjectMapper objectMapper;
    @Autowired private PirAppService pirAppService;

    @PostMapping(Constant.PIR_API_PREFIX + "/server")
    public ClientJobResponse pirServerController(@RequestBody ServerJobRequest serverJobRequest) {
        try {
            logger.info(
                    "WedprServerjob: serverJobRequest: {}.",
                    objectMapper.writeValueAsString(serverJobRequest));
            // 1. 根据请求，筛选数据，加密密钥，返回筛选结果及AES消息密文
            ServerOTResponse serverOTResponse = pirAppService.providerOtCipher(serverJobRequest);
            return new ClientJobResponse(WedprStatusEnum.SUCCESS, serverOTResponse);
        } catch (Exception e) {
            logger.warn(
                    "匿踪任务失败, jobID: {}, response: {}",
                    serverJobRequest.getJobId(),
                    WedprStatusEnum.SYSTEM_EXCEPTION.getMessage());
            return new ClientJobResponse(WedprStatusEnum.SYSTEM_EXCEPTION, e.getMessage());
        }
    }
}
