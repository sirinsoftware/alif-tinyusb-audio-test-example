# This file is derived from the TinyUSB project file
# examples/device/audio_test/CMakeLists.txt, which is distributed under the
# MIT licence; a verbatim copy is provided in LICENSE-MIT.txt.
#
# The modifications in this file were developed for the Alif Semiconductor
# platform. Published by Sirin Software as a collaboration snapshot.
#
# This repository combines material under several licences; see README.md
# and THIRD_PARTY_NOTICES.txt.

cmake_minimum_required(VERSION 3.20)

# Set Zephyr location
set(Zephyr_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../zephyr/share/zephyr-package/cmake)
# Set Zephyr build
set(RTOS zephyr)

# Include BSP
include(cmake/family_support.cmake)

# Get PROJECT name for the example (e.g. <BOARD>-<DIR_NAME>)
family_get_project_name(PROJECT ${CMAKE_CURRENT_LIST_DIR})
project(${PROJECT} C CXX ASM)

# Check this example is valid for the family and initializes the project
family_initialize_project(${PROJECT} ${CMAKE_CURRENT_LIST_DIR})

# Set executable
set(EXE_NAME app)

# Example source
target_sources(${EXE_NAME} PRIVATE
  ${CMAKE_CURRENT_SOURCE_DIR}/src/main.c
  ${CMAKE_CURRENT_SOURCE_DIR}/src/audio_device.c
  ${CMAKE_CURRENT_SOURCE_DIR}/src/usb_descriptors.c
  )

# Example include
target_include_directories(${EXE_NAME} PUBLIC
  ${CMAKE_CURRENT_SOURCE_DIR}/src
  )

# Configure compilation flags and libraries for Zephyr.
# See the corresponding function in hw/bsp/FAMILY/family.cmake for details.
family_configure_device_example(${EXE_NAME} ${RTOS})
