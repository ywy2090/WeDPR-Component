package com.wedpr.pir.demo;

import com.wedpr.pir.sdk.PirClient;
import com.wedpr.pir.sdk.entity.param.PirJobParam;
import com.wedpr.pir.sdk.entity.response.PirResultResponse;
import com.wedpr.pir.sdk.enums.ParamEnum;
import com.wedpr.pir.sdk.exception.WedprException;
import java.util.Arrays;

/**
 * @author zachma
 * @date 2024/8/22
 */
public class Demo {
    public static void main(String[] args) throws WedprException {
        testIdObfuscation();
        testIdFilter();
    }

    private static void testIdFilter() throws WedprException {
        PirJobParam pirJobParam = new PirJobParam();
        pirJobParam.setJobId("j-12345678912");
        pirJobParam.setJobType(ParamEnum.JobType.SearchValue.getValue());
        pirJobParam.setJobAlgorithmType(ParamEnum.AlgorithmType.idFilter.getValue());
        pirJobParam.setParticipateAgencyId("1002");
        pirJobParam.setDatasetId("t_login_token");
        pirJobParam.setJobCreator("1001");
        pirJobParam.setGatewayUrl("http://localhost:5831/api/pir/v3/server");
        pirJobParam.setSearchIdList(Arrays.asList("1", "20", "3", "456"));

        PirClient pirClient = new PirClient(pirJobParam);
        PirResultResponse pirResultResponse = pirClient.executePirJob();
        System.out.println(pirResultResponse);
    }

    private static void testIdObfuscation() throws WedprException {
        PirJobParam pirJobParam = new PirJobParam();
        pirJobParam.setJobId("j-12345678912");
        pirJobParam.setJobType(ParamEnum.JobType.SearchValue.getValue());
        pirJobParam.setJobAlgorithmType(ParamEnum.AlgorithmType.idObfuscation.getValue());
        pirJobParam.setParticipateAgencyId("1002");
        pirJobParam.setDatasetId("t_login_token");
        pirJobParam.setJobCreator("1001");
        pirJobParam.setGatewayUrl("http://localhost:5831/api/pir/v3/server");
        pirJobParam.setSearchIdList(Arrays.asList("1", "20", "3", "456"));

        PirClient pirClient = new PirClient(pirJobParam);
        PirResultResponse pirResultResponse = pirClient.executePirJob();
        System.out.println(pirResultResponse);
    }
}
