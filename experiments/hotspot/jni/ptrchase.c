#include <jni.h>

static jfieldID fid_next = NULL;
static jfieldID fid_value = NULL;

JNIEXPORT void JNICALL Java_BundleBench_initIDs(JNIEnv *env, jclass cls, jclass nodeClass) {
    (void)cls;
    fid_next = (*env)->GetFieldID(env, nodeClass, "next", "LBundleBench$Node;");
    fid_value = (*env)->GetFieldID(env, nodeClass, "value", "I");
}

JNIEXPORT jint JNICALL Java_BundleBench_chase8(JNIEnv *env, jclass cls, jobject p) {
    (void)cls;
    // Assume non-null ring; no null checks to emulate "contract" semantics.
    jobject p1 = (*env)->GetObjectField(env, p, fid_next);
    jobject p2 = (*env)->GetObjectField(env, p1, fid_next);
    jobject p3 = (*env)->GetObjectField(env, p2, fid_next);
    jobject p4 = (*env)->GetObjectField(env, p3, fid_next);
    jobject p5 = (*env)->GetObjectField(env, p4, fid_next);
    jobject p6 = (*env)->GetObjectField(env, p5, fid_next);
    jobject p7 = (*env)->GetObjectField(env, p6, fid_next);
    jobject p8 = (*env)->GetObjectField(env, p7, fid_next);
    return (*env)->GetIntField(env, p8, fid_value);
}
