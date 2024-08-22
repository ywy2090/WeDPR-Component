package com.webank.wedpr.pir.crypto.service;

import com.wedpr.pir.sdk.entity.request.ServerOTRequest;
import com.wedpr.pir.sdk.entity.response.ServerOTResponse;
import com.wedpr.pir.sdk.exception.WedprException;

/**
 * @author zachma
 * @date 2024/8/19
 */
public interface PirOTService {
    /**
     * @param serverOTRequest
     * @return PirOTResponse
     * @throws WedprException
     */
    ServerOTResponse runServerOTParam(ServerOTRequest serverOTRequest) throws WedprException;

    /**
     * @param serverOTRequest
     * @return PirOTResponse
     * @throws WedprException
     */
    ServerOTResponse runServerOTCipher(ServerOTRequest serverOTRequest) throws WedprException;
}
