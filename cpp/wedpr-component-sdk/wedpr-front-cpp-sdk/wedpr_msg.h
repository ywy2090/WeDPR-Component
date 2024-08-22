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
 * @file wedpr_front_common.h
 * @author: yujiechen
 * @date 2024-08-22
 */

#ifndef __WEDPR_MSG_H__
#define __WEDPR_MSG_H__

#include "ppc-framework/libwrapper/Buffer.h"

#ifdef __cplusplus
extern "C" {
#endif

struct gateway_optional_header
{
    // the componentType
    uint8_t componentType;
    // the source nodeID that send the message
    OutputBuffer* srcNode;
    // the target nodeID that should receive the message
    OutputBuffer* dstNode;
    // the target agency that need receive the message
    OutputBuffer* dstInst;
};

struct gateway_msg_header
{
    // the msg version, used to support compatibility
    uint8_t version;
    // the traceID
    OutputBuffer* traceID;
    // the srcGwNode
    OutputBuffer* srcGwNode;
    // the dstGwNode
    OutputBuffer* dstGwNode;
    // the packetType
    uint16_t packetType;
    // the seq
    uint32_t seq;
    // the ttl
    int16_t ttl;
    // the ext(contains the router policy and response flag)
    uint16_t ext;
    //// the optional field(used to route between components and nodes)
    struct gateway_optional_header* optionalFields;
};

struct front_payload
{
    // the front payload version, used to support compatibility
    uint8_t version;
    // the topic
    OutputBuffer* topic;
    OutputBuffer* data;
};

struct wedpr_msg
{
    gateway_msg_header* header;
    front_payload* payload;
};
#ifdef __cplusplus
}
#endif
#endif
