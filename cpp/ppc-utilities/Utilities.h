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
 * @file Utilitiles.cpp
 * @author: yujiechen
 * @date 2024-08-23
 */
#pragma once

#include "ppc-framework/Common.h"

namespace ppc
{
inline uint64_t decodeNetworkBuffer(
    bcos::bytes& _result, bcos::byte const* buffer, unsigned int bufferLen, uint64_t const offset)
{
    CHECK_OFFSET_WITH_THROW_EXCEPTION(offset, bufferLen);
    auto dataLen =
        boost::asio::detail::socket_ops::network_to_host_short(*((uint16_t*)buffer + offset));
    offset += 2;
    CHECK_OFFSET_WITH_THROW_EXCEPTION(offset, bufferLen);
    buffer.insert(
        buffer.end(), (bcos::byte*)_buffer + offset, (bcos::byte*)_buffer + offset + dataLen);
    offset += dataLen;
    return offset;
}
}  // namespace ppc