file(GLOB_RECURSE SRCS *.cpp *.c)

# generate the static lib
add_library(${PPC_FRONT_C_SDK_STATIC_TARGET} ${SRCS})
target_link_libraries(${PPC_FRONT_C_SDK_STATIC_TARGET} PUBLIC ${BCOS_UTILITIES_TARGET})

# generate the shared lib
add_library(${PPC_FRONT_C_SDK_TARGET} SHARED ${SRCS})
target_link_libraries(${PPC_FRONT_C_SDK_TARGET} PUBLIC ${BCOS_UTILITIES_TARGET})