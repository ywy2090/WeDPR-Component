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
 * @file Message.h
 * @author: yujiechen
 * @date 2024-08-22
 */
#pragma once
#include <bcos-boostssl/interfaces/MessageFace.h>
#include <bcos-utilities/Common.h>
#include <memory>

namespace ppc::protocol
{
class MessageOptionalHeader
{
public:
    using Ptr = std::shared_ptr<MessageOptionalHeader>;
    MessageOptionalHeader() = default;
    virtual ~MessageOptionalHeader() = default;

    virtual bcos::bytes encode() const = 0;
    // the componentType
    virtual uint8_t componentType() const { return m_componentType; }
    // the source nodeID that send the message
    virtual bcos::bytes const& srcNode() const { return m_srcNode; }
    // the target nodeID that should receive the message
    virtual bcos::bytes const& dstNode() const { return m_dstNode; }
    // the target agency that need receive the message
    virtual bcos::bytes const& dstInst() const { return m_dstInst; }

protected:
    virtual uint32_t decode(bcos::bytesConstRef data) = 0;

protected:
    // the componentType
    uint8_t m_componentType;
    // the source nodeID that send the message
    bcos::bytes m_srcNode;
    // the target nodeID that should receive the message
    bcos::bytes m_dstNode;
    // the target agency that need receive the message
    bcos::bytes m_dstInst;
};
class MessageHeader
{
public:
    using Ptr = std::shared_ptr<MessageHeader>;
    MessageHeader() = default;
    virtual ~MessageHeader() = default;

    virtual bcos::bytes encode() const = 0;

    // the msg version, used to support compatibility
    virtual uint8_t version() const { return m_version; }
    // the traceID
    virtual std::string const& traceID() const { return m_traceID; }
    // the srcGwNode
    virtual bcos::bytes const& srcGwNode() const { return m_srcGwNode; }
    // the dstGwNode
    virtual bcos::bytes const& dstGwNode() const { return m_dstGwNode; }
    // the packetType
    virtual uint16_t packetType() const { return m_packetType; }
    // the ttl
    virtual int16_t ttl() const { return m_ttl; }
    // the ext(contains the router policy and response flag)
    virtual uint16_t ext() const { return m_ext; }
    //// the optional field(used to route between components and nodes)
    virtual MessageOptionalHeader::Ptr optionalFields() const { return m_optionalFields; }

    virtual uint32_t length() const { return m_length; }

    virtual void setVersion(uint16_t version) { m_version = version; }
    virtual void setPacketType(uint16_t packetType) { m_packetType = packetType; }
    // the seq is the traceID
    virtual void setTraceID(std::string traceID) { m_traceID = traceID; }
    virtual void setExt(uint16_t ext) { m_ext = ext; }

    uint64_t packetLen() const { return m_packetLen; }
    uint16_t headerLen() const { return m_headerLen; }

    virtual bool isRespPacket() const = 0;
    virtual void setRespPacket() = 0;

protected:
    virtual uint32_t decode(bcos::bytesConstRef data) = 0;

protected:
    // the msg version, used to support compatibility
    uint8_t m_version;
    // the traceID
    std::string m_traceID;
    // the srcGwNode
    bcos::bytes m_srcGwNode;
    // the dstGwNode
    bcos::bytes m_dstGwNode;
    // the packetType
    uint16_t m_packetType;
    // the ttl
    int16_t m_ttl;
    // the ext(contains the router policy and response flag)
    uint16_t m_ext;
    //// the optional field(used to route between components and nodes)
    MessageOptionalHeader::Ptr m_optionalFields;
    uint64_t m_packetLen;
    uint16_t m_headerLen;
};

class MessagePayload
{
public:
    using Ptr = std::shared_ptr<MessagePayload>;
    MessagePayload() = default;
    virtual ~MessagePayload() = default;

    virtual bcos::bytes encode() const = 0;

    // the version
    virtual uint8_t version() const { return m_version; }
    // the topic
    virtual std::string const& topic() const { return m_topic; }
    virtual bcos::bytes const& data() const { return m_data; }
    virtual uint32_t length() const { return m_length; }

protected:
    virtual uint32_t decode(uint32_t startPos, bcos::bytesConstRef data) = 0;

protected:
    // the front payload version, used to support compatibility
    uint8_t m_version;
    // the topic
    std::string m_topic;
    bcos::bytes m_data;
    uint32_t m_length;
};

class Message : virtual public bcos::boostssl::MessageFace
{
public:
    using Ptr = std::shared_ptr<Message>;
    Message() = default;
    ~Message() override {}

    virtual MessageHeader::Ptr header() const { return m_header; }
    virtual MessagePayLoad::Ptr payload() const { return m_payload; }

    uint16_t version() const override { return m_header->version(); }
    void setVersion(uint16_t version) override{m_header->setVersion(version)} uint16_t
        packetType() const override
    {
        return m_header->packetType();
    }
    void setPacketType(uint16_t packetType) override { m_header->setPacketType(packetType); }
    std::string const& seq() const override { return m_header->traceID(); }
    void setSeq(std::string traceID) override { m_header->setTraceID(traceID); }
    uint16_t ext() const override { return m_header->ext(); }
    void setExt(uint16_t ext) override { m_header->setExt(except); }

    bool isRespPacket() const override { return m_header->isRespPacket(); }
    void setRespPacket() override { m_header->setRespPacket(); }

    virtual uint32_t length() const override { return m_header->packetLen(); }
    std::shared_ptr<bcos::bytes> payload() const override { return m_payload; }
    void setPayload(std::shared_ptr<bcos::bytes> _payload) override
    {
        m_payload = std::move(_payload);
    }


protected:
    MessageHeader::Ptr m_header;
    std::shared_ptr<bcos::bytes> m_payload;
};

class MessageBuilder
{
public:
    MessageBuilder() = default;
    virtual ~MessageBuilder() = default;

    virtual Message::Ptr build() = 0;
}
}  // namespace ppc::protocol