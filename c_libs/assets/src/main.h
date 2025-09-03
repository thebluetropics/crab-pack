#include <stdint.h>

#if defined(_WIN32)
__declspec(dllexport) uint8_t apply_raw_squid_and_calamari(char* source_0, char* source_1, char* target);
#else
uint8_t apply_raw_squid_and_calamari(char* source_0, char* source_1, char* target);
#endif

#if defined(_WIN32)
__declspec(dllexport) uint8_t apply_fortress_bricks(char* source, char* target);
#else
uint8_t apply_fortress_bricks(char* source, char* target);
#endif

#if defined(_WIN32)
__declspec(dllexport) uint8_t apply_hunger_and_thirst(char* source, char* target);
#else
uint8_t apply_hunger_and_thirst(char* source, char* target);
#endif

#if defined(_WIN32)
__declspec(dllexport) uint8_t apply_bottle(char* source, char* target);
#else
uint8_t apply_bottle(char* source, char* target);
#endif

#if defined(_WIN32)
__declspec(dllexport) uint8_t apply_cloth(char* source, char* target);
#else
uint8_t apply_cloth(char* source, char* target);
#endif

#if defined(_WIN32)
__declspec(dllexport) uint8_t apply_single_pixel_crosshair(char* source, char* target);
#else
uint8_t apply_single_pixel_crosshair(char* source, char* target);
#endif
