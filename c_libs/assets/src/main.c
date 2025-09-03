#include "main.h"

#define STB_IMAGE_IMPLEMENTATION
#include "../vendor/stb_image.h"
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "../vendor/stb_image_write.h"

struct _image_t {
	int w, h, _n;
	uint8_t* ptr;
};

static inline void set_pixel(uint8_t *image, int w, int x, int y, uint8_t r, uint8_t g, uint8_t b, uint8_t a) {
	int idx = (y * w + x) * 4;
	image[idx + 0] = r;
	image[idx + 1] = g;
	image[idx + 2] = b;
	image[idx + 3] = a;
}

void overlay(uint8_t *a, uint8_t *b, int a_width, int a_height, int b_width, int offset_x, int offset_y) {
	for (int y = 0; y < a_height; y++) {
		for (int x = 0; x < a_width; x++) {
			int idx_b = ((offset_y + y) * b_width + (offset_x + x)) * 4;
			int idx_a = (y * a_width + x) * 4;
			memcpy(&b[idx_b], &a[idx_a], 4);
		}
	}
}

uint8_t apply_raw_squid_and_calamari(char* source_0, char* source_1, char* target) {
	uint8_t code = 0;

	struct _image_t items;
	items.ptr = stbi_load(target, &items.w, &items.h, &items._n, 4);

	if (!items.ptr) {
		code = 1;
		goto _exit;
	}

	struct _image_t raw_squid;
	raw_squid.ptr = stbi_load(source_0, &raw_squid.w, &raw_squid.h, &raw_squid._n, 4);

	if (!raw_squid.ptr) {
		code = 1;
		goto _exit;
	}

	struct _image_t calamari;
	calamari.ptr = stbi_load(source_1, &calamari.w, &calamari.h, &calamari._n, 4);

	if (!calamari.ptr) {
		code = 1;
		goto _exit;
	}

	overlay(raw_squid.ptr, items.ptr, raw_squid.w, raw_squid.h, items.w, 32, 240);
	overlay(calamari.ptr, items.ptr, calamari.w, calamari.h, items.w, 48, 240);

	if (!stbi_write_png(target, items.w, items.h, 4, items.ptr, items.w * 4)) {
		code = 1;
		goto _exit;
	}

_exit:
	stbi_image_free(items.ptr);
	stbi_image_free(raw_squid.ptr);
	stbi_image_free(calamari.ptr);

	return code;
}

uint8_t apply_cloth(char* source, char* target) {
	uint8_t code = 0;

	struct _image_t items;
	items.ptr = stbi_load(target, &items.w, &items.h, &items._n, 4);

	if (!items.ptr) {
		code = 1;
		goto _exit;
	}

	struct _image_t cloth;
	cloth.ptr = stbi_load(source, &cloth.w, &cloth.h, &cloth._n, 4);

	if (!cloth.ptr) {
		code = 1;
		goto _exit;
	}

	overlay(cloth.ptr, items.ptr, cloth.w, cloth.h, items.w, 80, 240);

	if (!stbi_write_png(target, items.w, items.h, 4, items.ptr, items.w * 4)) {
		code = 1;
		goto _exit;
	}

_exit:
	stbi_image_free(items.ptr);
	stbi_image_free(cloth.ptr);

	return code;
}

uint8_t apply_fortress_bricks(char* source, char* target) {
	uint8_t code = 0;

	struct _image_t terrain;
	terrain.ptr = stbi_load(target, &terrain.w, &terrain.h, &terrain._n, 4);

	if (!terrain.ptr) {
		code = 1;
		goto _exit;
	}

	struct _image_t fortress_bricks;
	fortress_bricks.ptr = stbi_load(source, &fortress_bricks.w, &fortress_bricks.h, &fortress_bricks._n, 4);

	if (!fortress_bricks.ptr) {
		code = 1;
		goto _exit;
	}

	overlay(fortress_bricks.ptr, terrain.ptr, fortress_bricks.w, fortress_bricks.h, terrain.w, 96, 160);

	if (!stbi_write_png(target, terrain.w, terrain.h, 4, terrain.ptr, terrain.w * 4)) {
		code = 1;
		goto _exit;
	}

_exit:
	stbi_image_free(terrain.ptr);
	stbi_image_free(fortress_bricks.ptr);

	return code;
}

uint8_t apply_hunger_and_thirst(char* source, char* target) {
	uint8_t code = 0;

	struct _image_t icons;
	icons.ptr = stbi_load(target, &icons.w, &icons.h, &icons._n, 4);

	if (!icons.ptr) {
		code = 1;
		goto _exit;
	}

	struct _image_t hunger_and_thirst;
	hunger_and_thirst.ptr = stbi_load(source, &hunger_and_thirst.w, &hunger_and_thirst.h, &hunger_and_thirst._n, 4);

	if (!hunger_and_thirst.ptr) {
		code = 1;
		goto _exit;
	}

	overlay(hunger_and_thirst.ptr, icons.ptr, hunger_and_thirst.w, hunger_and_thirst.h, icons.w, 16, 27);

	if (!stbi_write_png(target, icons.w, icons.h, 4, icons.ptr, icons.w * 4)) {
		code = 1;
		goto _exit;
	}

_exit:
	stbi_image_free(icons.ptr);
	stbi_image_free(hunger_and_thirst.ptr);

	return code;
}

uint8_t apply_bottle(char* source, char* target) {
	uint8_t code = 0;

	struct _image_t items;
	items.ptr = stbi_load(target, &items.w, &items.h, &items._n, 4);

	if (!items.ptr) {
		code = 1;
		goto _exit;
	}

	struct _image_t bottle;
	bottle.ptr = stbi_load(source, &bottle.w, &bottle.h, &bottle._n, 4);

	if (!bottle.ptr) {
		code = 1;
		goto _exit;
	}

	overlay(bottle.ptr, items.ptr, bottle.w, bottle.h, items.w, 64, 240);

	if (!stbi_write_png(target, items.w, items.h, 4, items.ptr, items.w * 4)) {
		code = 1;
		goto _exit;
	}

_exit:
	stbi_image_free(items.ptr);
	stbi_image_free(bottle.ptr);

	return code;
}

uint8_t apply_single_pixel_crosshair(char* source, char* target) {
	uint8_t code = 0;

	struct _image_t icons;
	icons.ptr = stbi_load(target, &icons.w, &icons.h, &icons._n, 4);

	if (!icons.ptr) {
		code = 1;
		goto _exit;
	}

	struct _image_t single_pixel_crosshair;
	single_pixel_crosshair.ptr = stbi_load(source, &single_pixel_crosshair.w, &single_pixel_crosshair.h, &single_pixel_crosshair._n, 4);

	if (!single_pixel_crosshair.ptr) {
		code = 1;
		goto _exit;
	}

	overlay(single_pixel_crosshair.ptr, icons.ptr, single_pixel_crosshair.w, single_pixel_crosshair.h, icons.w, 0, 0);

	if (!stbi_write_png(target, icons.w, icons.h, 4, icons.ptr, icons.w * 4)) {
		code = 1;
		goto _exit;
	}

_exit:
	stbi_image_free(icons.ptr);
	stbi_image_free(single_pixel_crosshair.ptr);

	return code;
}
