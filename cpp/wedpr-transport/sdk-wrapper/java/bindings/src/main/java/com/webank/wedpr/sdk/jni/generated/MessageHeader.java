/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (https://www.swig.org).
 * Version 4.2.1
 *
 * Do not make changes to this file unless you know what you are doing - modify
 * the SWIG interface file instead.
 * ----------------------------------------------------------------------------- */

package com.webank.wedpr.sdk.jni.generated;

public class MessageHeader {
    private transient long swigCPtr;
    private transient boolean swigCMemOwn;

    protected MessageHeader(long cPtr, boolean cMemoryOwn) {
        swigCMemOwn = cMemoryOwn;
        swigCPtr = cPtr;
    }

    protected static long getCPtr(MessageHeader obj) {
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
                wedpr_java_transportJNI.delete_MessageHeader(swigCPtr);
            }
            swigCPtr = 0;
        }
    }

    public void encode(ubytes buffer) {
        wedpr_java_transportJNI.MessageHeader_encode(
                swigCPtr, this, ubytes.getCPtr(buffer), buffer);
    }

    public long decode(SWIGTYPE_p_bcos__bytesConstRef data) {
        return wedpr_java_transportJNI.MessageHeader_decode(
                swigCPtr, this, SWIGTYPE_p_bcos__bytesConstRef.getCPtr(data));
    }

    public short version() {
        return wedpr_java_transportJNI.MessageHeader_version(swigCPtr, this);
    }

    public void setVersion(int version) {
        wedpr_java_transportJNI.MessageHeader_setVersion(swigCPtr, this, version);
    }

    public String traceID() {
        return wedpr_java_transportJNI.MessageHeader_traceID(swigCPtr, this);
    }

    public void setTraceID(String traceID) {
        wedpr_java_transportJNI.MessageHeader_setTraceID(swigCPtr, this, traceID);
    }

    public String srcGwNode() {
        return wedpr_java_transportJNI.MessageHeader_srcGwNode(swigCPtr, this);
    }

    public void setSrcGwNode(String srcGwNode) {
        wedpr_java_transportJNI.MessageHeader_setSrcGwNode(swigCPtr, this, srcGwNode);
    }

    public String dstGwNode() {
        return wedpr_java_transportJNI.MessageHeader_dstGwNode(swigCPtr, this);
    }

    public void setDstGwNode(String dstGwNode) {
        wedpr_java_transportJNI.MessageHeader_setDstGwNode(swigCPtr, this, dstGwNode);
    }

    public int packetType() {
        return wedpr_java_transportJNI.MessageHeader_packetType(swigCPtr, this);
    }

    public void setPacketType(int packetType) {
        wedpr_java_transportJNI.MessageHeader_setPacketType(swigCPtr, this, packetType);
    }

    public short ttl() {
        return wedpr_java_transportJNI.MessageHeader_ttl(swigCPtr, this);
    }

    public void setTTL(int ttl) {
        wedpr_java_transportJNI.MessageHeader_setTTL(swigCPtr, this, ttl);
    }

    public int ext() {
        return wedpr_java_transportJNI.MessageHeader_ext(swigCPtr, this);
    }

    public void setExt(int ext) {
        wedpr_java_transportJNI.MessageHeader_setExt(swigCPtr, this, ext);
    }

    public MessageOptionalHeader optionalField() {
        long cPtr = wedpr_java_transportJNI.MessageHeader_optionalField(swigCPtr, this);
        return (cPtr == 0) ? null : new MessageOptionalHeader(cPtr, true);
    }

    public void setOptionalField(MessageOptionalHeader optionalField) {
        wedpr_java_transportJNI.MessageHeader_setOptionalField(
                swigCPtr, this, MessageOptionalHeader.getCPtr(optionalField), optionalField);
    }

    public int length() {
        return wedpr_java_transportJNI.MessageHeader_length(swigCPtr, this);
    }

    public boolean isRespPacket() {
        return wedpr_java_transportJNI.MessageHeader_isRespPacket(swigCPtr, this);
    }

    public void setRespPacket() {
        wedpr_java_transportJNI.MessageHeader_setRespPacket(swigCPtr, this);
    }

    public SWIGTYPE_p_std__string_view srcP2PNodeIDView() {
        return new SWIGTYPE_p_std__string_view(
                wedpr_java_transportJNI.MessageHeader_srcP2PNodeIDView(swigCPtr, this), true);
    }

    public SWIGTYPE_p_std__string_view dstP2PNodeIDView() {
        return new SWIGTYPE_p_std__string_view(
                wedpr_java_transportJNI.MessageHeader_dstP2PNodeIDView(swigCPtr, this), true);
    }

    public int routeType() {
        return wedpr_java_transportJNI.MessageHeader_routeType(swigCPtr, this);
    }

    public void setRouteType(SWIGTYPE_p_ppc__protocol__RouteType type) {
        wedpr_java_transportJNI.MessageHeader_setRouteType(
                swigCPtr, this, SWIGTYPE_p_ppc__protocol__RouteType.getCPtr(type));
    }

    public boolean hasOptionalField() {
        return wedpr_java_transportJNI.MessageHeader_hasOptionalField(swigCPtr, this);
    }
}
