/**
 *  Copyright (C) 2023 WeDPR.
 *  SPDX-License-Identifier: Apache-2.0
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 *
 * @file wedpr_front_config.h
 * @author: yujiechen
 * @date 2024-08-22
 */

#ifndef __WEDPR_FRONT_CONFIG_H__
#define __WEDPR_FRONT_CONFIG_H__
#include "ppc-framework/libwrapper/Buffer.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief the gateway endpoint information
 *
 */
struct wedpr_gateway_endpoint
{
    InputBuffer const* host;
    uint16_t port;
};

struct wedpr_gateway_info
{
    struct wedpr_gateway_endpoint* gatewayEndpoints;
    uint16_t gatewayCount;
};

struct wedpr_front_config
{
    int threadPoolSize;
    // the agency id
    InputBuffer const* agencyID;
    // the gateway-endpoints
    struct wedpr_gateway_info* gateway_info;
};
#ifdef __cplusplus
}
#endif
#endif