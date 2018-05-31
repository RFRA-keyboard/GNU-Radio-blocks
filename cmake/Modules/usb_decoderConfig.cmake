INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_USB_DECODER usb_decoder)

FIND_PATH(
    USB_DECODER_INCLUDE_DIRS
    NAMES usb_decoder/api.h
    HINTS $ENV{USB_DECODER_DIR}/include
        ${PC_USB_DECODER_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    USB_DECODER_LIBRARIES
    NAMES gnuradio-usb_decoder
    HINTS $ENV{USB_DECODER_DIR}/lib
        ${PC_USB_DECODER_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(USB_DECODER DEFAULT_MSG USB_DECODER_LIBRARIES USB_DECODER_INCLUDE_DIRS)
MARK_AS_ADVANCED(USB_DECODER_LIBRARIES USB_DECODER_INCLUDE_DIRS)

