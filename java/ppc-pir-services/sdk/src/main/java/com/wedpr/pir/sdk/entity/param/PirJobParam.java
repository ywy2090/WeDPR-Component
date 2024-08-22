package com.wedpr.pir.sdk.entity.param;

import com.wedpr.pir.sdk.entity.request.PirBaseRequest;
import com.wedpr.pir.sdk.enums.ParamEnum;
import com.wedpr.pir.sdk.exception.WedprException;
import com.wedpr.pir.sdk.exception.WedprStatusEnum;
import com.wedpr.pir.sdk.helper.BasicTypeHelper;
import java.util.Arrays;
import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;

/**
 * @author zachma
 * @date 2024/8/19
 */
@Data
@EqualsAndHashCode(callSuper = true)
public class PirJobParam extends PirBaseRequest {

    private Integer filterLength = 4;

    private String gatewayUrl;

    private List<String> searchIdList;

    public void check() throws WedprException {
        if (BasicTypeHelper.isStringEmpty(gatewayUrl)) {
            throw new WedprException(WedprStatusEnum.CLIENT_PARAM_EXCEPTION, "访问gatewayUrl不能为空");
        }

        if (BasicTypeHelper.isStringEmpty(getJobId())) {
            throw new WedprException(WedprStatusEnum.CLIENT_PARAM_EXCEPTION, "jobId 不能为空");
        }

        if (Arrays.stream(ParamEnum.JobType.values())
                .noneMatch(enumValue -> enumValue.getValue().equals(getJobType()))) {
            throw new WedprException(WedprStatusEnum.CLIENT_PARAM_EXCEPTION, "jobType输入错误");
        }

        if (BasicTypeHelper.isStringEmpty(getParticipateAgencyId())) {
            throw new WedprException(WedprStatusEnum.CLIENT_PARAM_EXCEPTION, "数据机构Id 不能为空");
        }

        if (BasicTypeHelper.isStringEmpty(getDatasetId())) {
            throw new WedprException(WedprStatusEnum.CLIENT_PARAM_EXCEPTION, "datasetId 不能为空");
        }

        if (Arrays.stream(ParamEnum.AlgorithmType.values())
                .noneMatch(enumValue -> enumValue.getValue().equals(getJobAlgorithmType()))) {
            throw new WedprException(
                    WedprStatusEnum.CLIENT_PARAM_EXCEPTION, "jobAlgorithmType输入错误");
        }

        if (searchIdList == null || searchIdList.size() == 0) {
            throw new WedprException(WedprStatusEnum.CLIENT_PARAM_EXCEPTION, "searchId列表不能为空");
        }

        if (getJobAlgorithmType().equals(ParamEnum.AlgorithmType.idObfuscation.getValue())
                && getObfuscationOrder() == -1) {
            throw new WedprException(
                    WedprStatusEnum.CLIENT_PARAM_EXCEPTION, "哈希披露算法中, obfuscationOrder未设置");
        }
    }
}
