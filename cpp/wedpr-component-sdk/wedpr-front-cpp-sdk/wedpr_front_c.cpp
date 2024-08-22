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
 * @file wedpr_front_c.h
 * @author: yujiechen
 * @date 2024-08-22
 */
#include "wedpr_front_c.h"

/**
 * @brief create the wedpr_front using specified config
 *
 * @param config the config used to build the wedpr_front
 * @return void* the created wedpr_front
 */
void* wedpr_front_create(struct wedpr_front_config* config)
{
    return nullptr;
}

/**
 * @brief start the wedpr_front
 *
 * @param front the front to start
 */
void wedpr_front_start(void* front) {}

/**
 * @brief stop the wedpr_front
 *
 * @param front the front to stop
 */
void wedpr_front_stop(void* front) {}

/**
 * @brief destroy the wedpr_front
 *
 * @param front the front to destroy
 */
void wedpr_front_destroy(void* front) {}

/**
 * @brief register the topic handler
 *
 * @param front the front object
 * @param topic the topic
 * @param callback the callback called when receive specified topic
 */
void register_topic_handler(void* front, InputBuffer const* topic, wedpr_msg_handler_cb callback) {}

/**
 * @brief async send message
 *
 * @param front the front to send the message
 * @param routerPolicy the router policy:
 *              0: route by nodeID
 *              1: route by component
 *              2: route by agency
 * @param topic  the topic
 * @param dstInst the dst agency(must set when 'route by agency' and 'route by
 * component')
 * @param dstNodeID  the dst nodeID(must set when 'route by nodeID')
 * @param componentType the componentType(must set when 'route by component')
 * @param payload the payload to send
 * @param seq the message seq
 * @param timeout timeout
 * @param callback callback
 */
void async_send_message(void* front, int routerPolicy, InputBuffer const* topic,
    InputBuffer const* dstInst, InputBuffer const* dstNodeID, uint8_t componentType,
    InputBuffer const* payload, int seq, long timeout, wedpr_msg_handler_cb callback)
{}

// the sync interface for async_send_message
wedpr_msg* push(void* front, int routerPolicy, InputBuffer const* topic, InputBuffer const* dstInst,
    InputBuffer const* dstNodeID, uint8_t componentType, InputBuffer const* payload, int seq,
    long timeout)
{
    return nullptr;
}
