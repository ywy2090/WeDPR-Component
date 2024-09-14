/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (https://www.swig.org).
 * Version 4.2.1
 *
 * Do not make changes to this file unless you know what you are doing - modify
 * the SWIG interface file instead.
 * ----------------------------------------------------------------------------- */

package com.webank.wedpr.sdk.jni.generated;

public class MessageBuilder {
    private transient long swigCPtr;
    private transient boolean swigCMemOwn;

    protected MessageBuilder(long cPtr, boolean cMemoryOwn) {
        swigCMemOwn = cMemoryOwn;
        swigCPtr = cPtr;
    }

    protected static long getCPtr(MessageBuilder obj) {
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
                wedpr_java_transportJNI.delete_MessageBuilder(swigCPtr);
            }
            swigCPtr = 0;
        }
    }

    public Message build() {
        long cPtr = wedpr_java_transportJNI.MessageBuilder_build__SWIG_0(swigCPtr, this);
        return (cPtr == 0) ? null : new Message(cPtr, true);
    }

    public Message build(SWIGTYPE_p_bcos__bytesConstRef buffer) {
        long cPtr =
                wedpr_java_transportJNI.MessageBuilder_build__SWIG_1(
                        swigCPtr, this, SWIGTYPE_p_bcos__bytesConstRef.getCPtr(buffer));
        return (cPtr == 0) ? null : new Message(cPtr, true);
    }

    public Message build(
            SWIGTYPE_p_ppc__protocol__RouteType routeType,
            MessageOptionalHeader routeInfo,
            ubytes payload) {
        long cPtr =
                wedpr_java_transportJNI.MessageBuilder_build__SWIG_2(
                        swigCPtr,
                        this,
                        SWIGTYPE_p_ppc__protocol__RouteType.getCPtr(routeType),
                        MessageOptionalHeader.getCPtr(routeInfo),
                        routeInfo,
                        ubytes.swigRelease(payload),
                        payload);
        return (cPtr == 0) ? null : new Message(cPtr, true);
    }

    public void disOwnMemory() {
        swigSetCMemOwn(false);
    }
}
