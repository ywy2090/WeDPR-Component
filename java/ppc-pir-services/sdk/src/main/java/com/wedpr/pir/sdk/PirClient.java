package com.wedpr.pir.sdk;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.sun.org.slf4j.internal.Logger;
import com.sun.org.slf4j.internal.LoggerFactory;
import com.wedpr.pir.sdk.entity.body.SimpleEntity;
import com.wedpr.pir.sdk.entity.param.PirJobParam;
import com.wedpr.pir.sdk.entity.request.ServerJobRequest;
import com.wedpr.pir.sdk.entity.response.ClientOTResponse;
import com.wedpr.pir.sdk.entity.response.PirResultResponse;
import com.wedpr.pir.sdk.exception.WedprException;
import com.wedpr.pir.sdk.exception.WedprStatusEnum;
import com.wedpr.pir.sdk.gateway.GatewayClient;
import com.wedpr.pir.sdk.service.PirJobService;
import java.util.Objects;

/**
 * @author zachma
 * @date 2024/8/19
 */
public class PirClient {
    private static final Logger logger = LoggerFactory.getLogger(PirClient.class);
    private final PirJobService pirJobService;

    public PirClient(PirJobParam pirJobParam) throws WedprException {
        pirJobParam.check();
        this.pirJobService = new PirJobService(pirJobParam);
    }

    public PirResultResponse executePirJob() throws WedprException {
        try {
            ClientOTResponse otParamResponse = pirJobService.requesterOtCipher();
            PirJobParam pirJobParam = pirJobService.getPirJobParam();
            ServerJobRequest serverJobRequest =
                    generatePirJobRequestFromJobAndOTParam(pirJobParam, otParamResponse);
            logger.debug("executePirJob start: ", serverJobRequest);

            String pirUrl = pirJobParam.getGatewayUrl();
            ObjectMapper objectMapper = new ObjectMapper();
            String body = objectMapper.writeValueAsString(serverJobRequest);
            SimpleEntity otResult =
                    GatewayClient.sendPostRequestWithRetry(pirUrl, body, SimpleEntity.class);
            logger.debug("executePirJob success return: ", otResult);
            if (Objects.isNull(otResult)
                    || !otResult.getCode().equals(WedprStatusEnum.SUCCESS.getCode())) {
                throw new WedprException(WedprStatusEnum.TASK_EXECUTE_ERROR);
            }
            return pirJobService.requesterOtRecover(otParamResponse, pirJobParam, otResult);
        } catch (Exception e) {
            logger.error("executePirJob cause exception: ", e.getMessage());
            throw new WedprException(WedprStatusEnum.CALL_PSI_ERROR);
        }
    }

    /** 根据 ClientOTResponse 和 PirJobParam 构建PirJobRequest */
    private ServerJobRequest generatePirJobRequestFromJobAndOTParam(
            PirJobParam pirJobParam, ClientOTResponse otParamResponse) {
        ServerJobRequest serverJobRequest = new ServerJobRequest();
        serverJobRequest.setJobId(pirJobParam.getJobId());
        serverJobRequest.setParticipateAgencyId(pirJobParam.getParticipateAgencyId());
        serverJobRequest.setDatasetId(pirJobParam.getDatasetId());
        serverJobRequest.setJobCreator(pirJobParam.getJobCreator());
        serverJobRequest.setJobAlgorithmType(pirJobParam.getJobAlgorithmType());
        serverJobRequest.setX(otParamResponse.getX());
        serverJobRequest.setY(otParamResponse.getY());
        serverJobRequest.setDataBodyList(otParamResponse.getDataBodyList());
        for (int i = 0; i < serverJobRequest.getDataBodyList().size(); i++) {
            serverJobRequest.getDataBodyList().get(i).setIdIndex(0);
        }
        return serverJobRequest;
    }
}
