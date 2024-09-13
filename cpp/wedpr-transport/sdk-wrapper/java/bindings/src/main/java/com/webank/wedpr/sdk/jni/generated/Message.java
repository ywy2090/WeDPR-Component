/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (https://www.swig.org).
 * Version 4.2.1
 *
 * Do not make changes to this file unless you know what you are doing - modify
 * the SWIG interface file instead.
 * ----------------------------------------------------------------------------- */

package com.webank.wedpr.sdk.jni.generated;

public class Message {
    private transient long swigCPtr;
    private transient boolean swigCMemOwn;

    protected Message(long cPtr, boolean cMemoryOwn) {
        swigCMemOwn = cMemoryOwn;
        swigCPtr = cPtr;
    }

    protected static long getCPtr(Message obj) {
        return (obj == null) ? 0 : obj.swigCPtr;
    }

    protected void swigSetCMemOwn(boolean own) {
        swigCMemOwn = own;
    }

    @SuppressWarnings({"deprecation", "removal"})
    protected void finalize() {
        delete();
    }

    public synchronized void delete() {
        if (swigCPtr != 0) {
            if (swigCMemOwn) {
                swigCMemOwn = false;
                wedpr_java_transportJNI.delete_Message(swigCPtr);
            }
            swigCPtr = 0;
        }
    }

    public MessageHeader header() {
        long cPtr = wedpr_java_transportJNI.Message_header(swigCPtr, this);
        return (cPtr == 0) ? null : new MessageHeader(cPtr, true);
    }

    public void setHeader(MessageHeader header) {
        wedpr_java_transportJNI.Message_setHeader(
                swigCPtr, this, MessageHeader.getCPtr(header), header);
    }

    /** the overloaed implementation === */
    public int version() {
        return wedpr_java_transportJNI.Message_version(swigCPtr, this);
    }

    public void setVersion(int version) {
        wedpr_java_transportJNI.Message_setVersion(swigCPtr, this, version);
    }

    public int packetType() {
        return wedpr_java_transportJNI.Message_packetType(swigCPtr, this);
    }

    public void setPacketType(int packetType) {
        wedpr_java_transportJNI.Message_setPacketType(swigCPtr, this, packetType);
    }

    public String seq() {
        return wedpr_java_transportJNI.Message_seq(swigCPtr, this);
    }

    public void setSeq(String traceID) {
        wedpr_java_transportJNI.Message_setSeq(swigCPtr, this, traceID);
    }

    public int ext() {
        return wedpr_java_transportJNI.Message_ext(swigCPtr, this);
    }

    public void setExt(int ext) {
        wedpr_java_transportJNI.Message_setExt(swigCPtr, this, ext);
    }

    public boolean isRespPacket() {
        return wedpr_java_transportJNI.Message_isRespPacket(swigCPtr, this);
    }

    public void setRespPacket() {
        wedpr_java_transportJNI.Message_setRespPacket(swigCPtr, this);
    }

    public long length() {
        return wedpr_java_transportJNI.Message_length(swigCPtr, this);
    }

    public ubytes payload() {
        long cPtr = wedpr_java_transportJNI.Message_payload(swigCPtr, this);
        return (cPtr == 0) ? null : new ubytes(cPtr, true);
    }

    public byte[] payloadBuffer() {
        return wedpr_java_transportJNI.Message_payloadBuffer(swigCPtr, this);
    }

    public void setPayload(ubytes _payload) {
        wedpr_java_transportJNI.Message_setPayload(
                swigCPtr, this, ubytes.getCPtr(_payload), _payload);
    }

    public void setFrontMessage(MessagePayload frontMessage) {
        wedpr_java_transportJNI.Message_setFrontMessage(
                swigCPtr, this, MessagePayload.getCPtr(frontMessage), frontMessage);
    }

    public MessagePayload frontMessage() {
        long cPtr = wedpr_java_transportJNI.Message_frontMessage(swigCPtr, this);
        return (cPtr == 0) ? null : new MessagePayload(cPtr, true);
    }

    public boolean encode(ubytes _buffer) {
        return wedpr_java_transportJNI.Message_encode__SWIG_0(
                swigCPtr, this, ubytes.getCPtr(_buffer), _buffer);
    }

    public boolean encode(SWIGTYPE_p_bcos__boostssl__EncodedMsg _encodedMsg) {
        return wedpr_java_transportJNI.Message_encode__SWIG_1(
                swigCPtr, this, SWIGTYPE_p_bcos__boostssl__EncodedMsg.getCPtr(_encodedMsg));
    }

    public long decode(SWIGTYPE_p_bcos__bytesConstRef _buffer) {
        return wedpr_java_transportJNI.Message_decode(
                swigCPtr, this, SWIGTYPE_p_bcos__bytesConstRef.getCPtr(_buffer));
    }
}
