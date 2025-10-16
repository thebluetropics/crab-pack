from modmaker import *
import mod

def apply():
	if not mod.config.is_feature_enabled('block.mortar'):
		return

	cf = load_class_file(mod.config.path('stage/client/cv.class'))
	cp_cache = cp_init_cache(cf[0x04])

	_modify_render_1_method(cf, cp_cache)
	_modify_render_2_method(cf, cp_cache)
	_modify_is_side_lit_method(cf, cp_cache)

	cf[0x0d].append(_create_render_mortar_method(cf, cp_cache))
	cf[0x0c] = len(cf[0x0d]).to_bytes(2)

	with open(mod.config.path('stage/client/cv.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print('Patched client:cv.class → net.minecraft.client.render.BlockRenderManager')

def _modify_render_1_method(cf, cp_cache):
	m = get_method(cf, cp_cache, 'b', '(Luu;III)Z')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x03] = a_code[0x03][0:18] + assemble_code(cf, cp_cache, 0, 18, [
		['iload', 5],
		['bipush', 50],
		['if_icmpne', 'skip'],

		'aload_0',
		'aload_1',
		['iload', 2],
		['iload', 3],
		['iload', 4],
		['invokevirtual', 'cv', 'renderMortar', '(Luu;III)Z'],
		'ireturn',

		['label', 'skip'],
	]) + a_code[0x03][18:324]

	# update code length
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove line number table
	for i, attribute in enumerate(a_code[0x07]):
		if get_utf8_at(cp_cache, int.from_bytes(attribute[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a_code[0x06] = len(a_code[0x07]).to_bytes(2)

	# update code attribute
	a[0x02] = a_code_assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

def _render_face(
		nx, ny, nz,
		v0_x, v0_y, v0_z, v0_u, v0_v, v0_u_offset, v0_v_offset,
		v1_x, v1_y, v1_z, v1_u, v1_v, v1_u_offset, v1_v_offset,
		v2_x, v2_y, v2_z, v2_u, v2_v, v2_u_offset, v2_v_offset,
		v3_x, v3_y, v3_z, v3_u, v3_v, v3_u_offset, v3_v_offset
):
	return [
		['aload', 4],
		['invokevirtual', 'nw', 'b', '()V'],

		['aload', 4],
		nx,
		ny,
		nz,
		['invokevirtual', 'nw', 'b', '(FFF)V'],

		['aload', 4],
		['ldc2_w.f64', v0_x / 16.0],
		['ldc2_w.f64', v0_y / 16.0],
		['ldc2_w.f64', v0_z / 16.0],
		['ldc2_w.f64', v0_u / 256.0], ['ldc2_w.f64', (v0_u_offset / 16.0) * (16.0 / 256.0)], 'dadd',
		['ldc2_w.f64', v0_v / 256.0], ['ldc2_w.f64', (v0_v_offset / 16.0) * (16.0 / 256.0)], 'dadd',
		['invokevirtual', 'nw', 'a', '(DDDDD)V'],

		['aload', 4],
		['ldc2_w.f64', v1_x / 16.0],
		['ldc2_w.f64', v1_y / 16.0],
		['ldc2_w.f64', v1_z / 16.0],
		['ldc2_w.f64', v1_u / 256.0], ['ldc2_w.f64', (v1_u_offset / 16.0) * (16.0 / 256.0)], 'dadd',
		['ldc2_w.f64', v1_v / 256.0], ['ldc2_w.f64', (v1_v_offset / 16.0) * (16.0 / 256.0)], 'dadd',
		['invokevirtual', 'nw', 'a', '(DDDDD)V'],

		['aload', 4],
		['ldc2_w.f64', v2_x / 16.0],
		['ldc2_w.f64', v2_y / 16.0],
		['ldc2_w.f64', v2_z / 16.0],
		['ldc2_w.f64', v2_u / 256.0], ['ldc2_w.f64', (v2_u_offset / 16.0) * (16.0 / 256.0)], 'dadd',
		['ldc2_w.f64', v2_v / 256.0], ['ldc2_w.f64', (v2_v_offset / 16.0) * (16.0 / 256.0)], 'dadd',
		['invokevirtual', 'nw', 'a', '(DDDDD)V'],

		['aload', 4],
		['ldc2_w.f64', v3_x / 16.0],
		['ldc2_w.f64', v3_y / 16.0],
		['ldc2_w.f64', v3_z / 16.0],
		['ldc2_w.f64', v3_u / 256.0], ['ldc2_w.f64', (v3_u_offset / 16.0) * (16.0 / 256.0)], 'dadd',
		['ldc2_w.f64', v3_v / 256.0], ['ldc2_w.f64', (v3_v_offset / 16.0) * (16.0 / 256.0)], 'dadd',
		['invokevirtual', 'nw', 'a', '(DDDDD)V'],

		['aload', 4],
		['invokevirtual', 'nw', 'a', '()V']
	]

def _modify_render_2_method(cf, cp_cache):
	m = get_method(cf, cp_cache, 'a', '(Luu;IF)V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x00] = (20).to_bytes(2)
	a_code[0x03] = a_code[0x03][0:83] + assemble_code(cf, cp_cache, 0, 83, [
		['iload', 5],
		['bipush', 50],
		['if_icmpne', 'skip_c'],

		['ldc_w.f32', -0.5],
		['ldc_w.f32', -0.5],
		['ldc_w.f32', -0.5],
		['invokestatic', 'org/lwjgl/opengl/GL11', 'glTranslatef', '(FFF)V'],

		*_render_face(
			'fconst_0', ['ldc_w.f32', 1.0], 'fconst_0',
			1.0, 6.0, 1.0, 64.0, 176.0, 1.0, 1.0,
			1.0, 6.0, 15.0, 64.0, 176.0, 1.0, 15.0,
			15.0, 6.0, 15.0, 64.0, 176.0, 15.0, 15.0,
			15.0, 6.0, 1.0, 64.0, 176.0, 15.0, 1.0,
		),

		*_render_face(
			'fconst_0', ['ldc_w.f32', 1.0], 'fconst_0',
			3.0, 2.0, 3.0, 80.0, 176.0, 3.0, 3.0,
			3.0, 2.0, 13.0, 80.0, 176.0, 13.0, 13.0,
			13.0, 2.0, 13.0, 80.0, 176.0, 13.0, 13.0,
			13.0, 2.0, 3.0, 80.0, 176.0, 13.0, 3.0,
		),

		*_render_face(
			'fconst_0', ['ldc_w.f32', -1.0], 'fconst_0',
			1.0, 0.0, 15.0, 96.0, 176.0, 1.0, 15.0,
			1.0, 0.0, 1.0, 96.0, 176.0, 1.0, 1.0,
			15.0, 0.0, 1.0, 96.0, 176.0, 15.0, 1.0,
			15.0, 0.0, 15.0, 96.0, 176.0, 15.0, 15.0,
		),

		*_render_face(
			['ldc_w.f32', -1.0], 'fconst_0', 'fconst_0',
			1.0, 6.0, 15.0, 112.0, 176.0, 15.0, 10.0,
			1.0, 6.0, 1.0, 112.0, 176.0, 1.0, 10.0,
			1.0, 0.0, 1.0, 112.0, 176.0, 1.0, 16.0,
			1.0, 0.0, 15.0, 112.0, 176.0, 15.0, 16.0,
		),

		*_render_face(
			['ldc_w.f32', -1.0], 'fconst_0', 'fconst_0',
			13.0, 6.0, 15.0, 112.0, 176.0, 15.0, 10.0,
			13.0, 6.0, 1.0, 112.0, 176.0, 1.0, 10.0,
			13.0, 0.0, 1.0, 112.0, 176.0, 1.0, 16.0,
			13.0, 0.0, 15.0, 112.0, 176.0, 15.0, 16.0,
		),

		*_render_face(
			['ldc_w.f32', 1.0], 'fconst_0', 'fconst_0',
			15.0, 0.0, 15.0, 112.0, 176.0, 15.0, 16.0,
			15.0, 0.0, 1.0, 112.0, 176.0, 1.0, 16.0,
			15.0, 6.0, 1.0, 112.0, 176.0, 1.0, 10.0,
			15.0, 6.0, 15.0, 112.0, 176.0, 15.0, 10.0,
		),

		*_render_face(
			['ldc_w.f32', 1.0], 'fconst_0', 'fconst_0',
			3.0, 0.0, 15.0, 112.0, 176.0, 15.0, 16.0,
			3.0, 0.0, 1.0, 112.0, 176.0, 1.0, 16.0,
			3.0, 6.0, 1.0, 112.0, 176.0, 1.0, 10.0,
			3.0, 6.0, 15.0, 112.0, 176.0, 15.0, 10.0,
		),

		*_render_face(
			'fconst_0', 'fconst_0', ['ldc_w.f32', -1.0],
			1.0, 6.0, 1.0, 112.0, 176.0, 1.0, 10.0,
			15.0, 6.0, 1.0, 112.0, 176.0, 15.0, 10.0,
			15.0, 0.0, 1.0, 112.0, 176.0, 15.0, 16.0,
			1.0, 0.0, 1.0, 112.0, 176.0, 1.0, 16.0,
		),

		*_render_face(
			'fconst_0', 'fconst_0', ['ldc_w.f32', -1.0],
			1.0, 6.0, 13.0, 112.0, 176.0, 1.0, 10.0,
			15.0, 6.0, 13.0, 112.0, 176.0, 15.0, 10.0,
			15.0, 0.0, 13.0, 112.0, 176.0, 15.0, 16.0,
			1.0, 0.0, 13.0, 112.0, 176.0, 1.0, 16.0,
		),

		*_render_face(
			'fconst_0', 'fconst_0', ['ldc_w.f32', 1.0],
			1.0, 6.0, 15.0, 112.0, 176.0, 1.0, 10.0,
			1.0, 0.0, 15.0, 112.0, 176.0, 1.0, 16.0,
			15.0, 0.0, 15.0, 112.0, 176.0, 15.0, 16.0,
			15.0, 6.0, 15.0, 112.0, 176.0, 15.0, 10.0,
		),

		*_render_face(
			'fconst_0', 'fconst_0', ['ldc_w.f32', 1.0],
			1.0, 6.0, 3.0, 112.0, 176.0, 1.0, 10.0,
			1.0, 0.0, 3.0, 112.0, 176.0, 1.0, 16.0,
			15.0, 0.0, 3.0, 112.0, 176.0, 15.0, 16.0,
			15.0, 6.0, 3.0, 112.0, 176.0, 15.0, 10.0,
		),

		['ldc_w.f32', 0.5],
		['ldc_w.f32', 0.5],
		['ldc_w.f32', 0.5],
		['invokestatic', 'org/lwjgl/opengl/GL11', 'glTranslatef', '(FFF)V'],

		'return',

		['label', 'skip_c'],
	]) + a_code[0x03][83:1411]

	# update code length
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove line number table
	for i, attribute in enumerate(a_code[0x07]):
		if get_utf8_at(cp_cache, int.from_bytes(attribute[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a_code[0x06] = len(a_code[0x07]).to_bytes(2)

	# update code attribute
	a[0x02] = a_code_assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

def _modify_is_side_lit_method(cf, cp_cache):
	m = get_method(cf, cp_cache, 'a', '(I)Z')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x03] = assemble_code(cf, cp_cache, 0, 0, [
		'iload_0',
		['bipush', 50],
		['if_icmpne', 'skip_a'],
		'iconst_1',
		'ireturn',
		['label', 'skip_a']
	]) + a_code[0x03][0:40]

	# update code length
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove line number table
	for i, attribute in enumerate(a_code[0x07]):
		if get_utf8_at(cp_cache, int.from_bytes(attribute[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a_code[0x06] = len(a_code[0x07]).to_bytes(2)

	# update code attribute
	a[0x02] = a_code_assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

def _texture_override(index, label):
	return [
		['sipush', index],
		['istore', 7],

		'aload_0',
		['getfield', 'cv', 'd', 'I'],
		['iflt', label],

		'aload_0',
		['getfield', 'cv', 'd', 'I'],
		['istore', 7],

		['label', label],
		['iload', 7],
		['bipush', 15],
		'iand',
		'iconst_4',
		'ishl',
		['istore', 8],

		['iload', 7],
		['sipush', 240],
		'iand',
		['istore', 9]
	]

def _fn_vertex(x, y, z, u_offset, v_offset):
	return [
		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w.f64', x / 16.0], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w.f64', y / 16.0], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w.f64', z / 16.0], 'dadd',
		['iload', 8], 'i2d', ['ldc2_w.f64', 256.0], 'ddiv', ['ldc2_w.f64', (u_offset / 16.0) * (16.0 / 256.0)], 'dadd',
		['iload', 9], 'i2d', ['ldc2_w.f64', 256.0], 'ddiv', ['ldc2_w.f64', (v_offset / 16.0) * (16.0 / 256.0)], 'dadd',
		['invokevirtual', 'nw', 'a', '(DDDDD)V'],
	]

def _fn_set_tessellator_color(*color):
	return [
		['aload', 5],
		*color,
		['invokevirtual', 'nw', 'a', '(FFF)V']
	]

def _create_render_mortar_method(cf, cp_cache):
	m = create_method(cf, cp_cache, ['public'], 'renderMortar', '(Luu;III)Z')

	code = [
		['getstatic', 'nw', 'a', 'Lnw;'],
		['astore', 5],

		['aload', 1],
		'aload_0',
		['getfield', 'cv', 'c', 'Lxp;'],
		['iload', 2],
		['iload', 3],
		['iload', 4],
		['invokevirtual', 'uu', 'd', '(Lxp;III)F'],
		['fstore', 6],

		'aload_0',
		['getfield', 'cv', 'c', 'Lxp;'],
		['iload', 2],
		['iload', 3],
		['iload', 4],
		['invokeinterface', 'xp', 'e', '(III)I', 4],
		['istore', 10],

		['invokestatic', 'net/minecraft/client/Minecraft','v', '()Z'],
		['ifeq', 'skip_smooth_rendering'],

		*_texture_override(180, 'skip_1_smooth'),

		*_fn_set_tessellator_color(['fload', 6], ['fload', 6], ['fload', 6]),
		*_fn_vertex(1.0, 6.0, 1.0, 1.0, 1.0),
		*_fn_vertex(1.0, 6.0, 15.0, 1.0, 15.0),
		*_fn_vertex(15.0, 6.0, 15.0, 15.0, 15.0),
		*_fn_vertex(15.0, 6.0, 1.0, 15.0, 1.0),

		*_texture_override(181, 'skip_2_smooth'),

		*_fn_set_tessellator_color(['fload', 6], ['fload', 6], ['fload', 6]),
		*_fn_vertex(3.0, 2.0, 3.0, 3.0, 3.0),
		*_fn_vertex(3.0, 2.0, 13.0, 3.0, 13.0),
		*_fn_vertex(13.0, 2.0, 13.0, 13.0, 13.0),
		*_fn_vertex(13.0, 2.0, 3.0, 13.0, 3.0),

		*_texture_override(182, 'skip_bottom_smooth'),

		*_fn_set_tessellator_color(['fload', 6], ['fload', 6], ['fload', 6]),
		*_fn_vertex(1.0, 0.0, 15.0, 1.0, 15.0),
		*_fn_vertex(1.0, 0.0, 1.0, 1.0, 1.0),
		*_fn_vertex(15.0, 0.0, 1.0, 15.0, 1.0),
		*_fn_vertex(15.0, 0.0, 15.0, 15.0, 15.0),

		*_texture_override(183, 'skip_north_1_smooth'),

		*_fn_set_tessellator_color(['fload', 6], ['fload', 6], ['fload', 6]),
		*_fn_vertex(1.0, 6.0, 15.0, 15.0, 10.0),
		*_fn_vertex(1.0, 6.0, 1.0, 1.0, 10.0),
		*_fn_set_tessellator_color(['fload', 6], ['ldc_w.f32', 0.25], 'fsub', ['fload', 6], ['ldc_w.f32', 0.25], 'fsub', ['fload', 6], ['ldc_w.f32', 0.25], 'fsub'),
		*_fn_vertex(1.0, 0.0, 1.0, 1.0, 16.0),
		*_fn_vertex(1.0, 0.0, 15.0, 15.0, 16.0),

		*_texture_override(183, 'skip_north_2_smooth'),

		*_fn_set_tessellator_color(['fload', 6], ['fload', 6], ['fload', 6]),
		*_fn_vertex(13.0, 6.0, 15.0, 15.0, 10.0),
		*_fn_vertex(13.0, 6.0, 1.0, 1.0, 10.0),
		*_fn_set_tessellator_color(['fload', 6], ['ldc_w.f32', 0.25], 'fsub', ['fload', 6], ['ldc_w.f32', 0.25], 'fsub', ['fload', 6], ['ldc_w.f32', 0.25], 'fsub'),
		*_fn_vertex(13.0, 0.0, 1.0, 1.0, 16.0),
		*_fn_vertex(13.0, 0.0, 15.0, 15.0, 16.0),

		*_texture_override(183, 'skip_south_1_smooth'),

		*_fn_set_tessellator_color(['fload', 6], ['ldc_w.f32', 0.25], 'fsub', ['fload', 6], ['ldc_w.f32', 0.25], 'fsub', ['fload', 6], ['ldc_w.f32', 0.25], 'fsub'),
		*_fn_vertex(15.0, 0.0, 15.0, 15.0, 16.0),
		*_fn_vertex(15.0, 0.0, 1.0, 1.0, 16.0),
		*_fn_set_tessellator_color(['fload', 6], ['fload', 6], ['fload', 6]),
		*_fn_vertex(15.0, 6.0, 1.0, 1.0, 10.0),
		*_fn_vertex(15.0, 6.0, 15.0, 15.0, 10.0),

		*_texture_override(183, 'skip_south_2_smooth'),

		*_fn_set_tessellator_color(['fload', 6], ['ldc_w.f32', 0.25], 'fsub', ['fload', 6], ['ldc_w.f32', 0.25], 'fsub', ['fload', 6], ['ldc_w.f32', 0.25], 'fsub'),
		*_fn_vertex(3.0, 0.0, 15.0, 15.0, 16.0),
		*_fn_vertex(3.0, 0.0, 1.0, 1.0, 16.0),
		*_fn_set_tessellator_color(['fload', 6], ['fload', 6], ['fload', 6]),
		*_fn_vertex(3.0, 6.0, 1.0, 1.0, 10.0),
		*_fn_vertex(3.0, 6.0, 15.0, 15.0, 10.0),

		*_texture_override(183, 'skip_east_1_smooth'),

		*_fn_set_tessellator_color(['fload', 6], ['fload', 6], ['fload', 6]),
		*_fn_vertex(1.0, 6.0, 1.0, 1.0, 10.0),
		*_fn_vertex(15.0, 6.0, 1.0, 15.0, 10.0),
		*_fn_set_tessellator_color(['fload', 6], ['ldc_w.f32', 0.25], 'fsub', ['fload', 6], ['ldc_w.f32', 0.25], 'fsub', ['fload', 6], ['ldc_w.f32', 0.25], 'fsub'),
		*_fn_vertex(15.0, 0.0, 1.0, 15.0, 16.0),
		*_fn_vertex(1.0, 0.0, 1.0, 1.0, 16.0),

		*_texture_override(183, 'skip_east_2_smooth'),

		*_fn_set_tessellator_color(['fload', 6], ['fload', 6], ['fload', 6]),
		*_fn_vertex(1.0, 6.0, 13.0, 1.0, 10.0),
		*_fn_vertex(15.0, 6.0, 13.0, 15.0, 10.0),
		*_fn_set_tessellator_color(['fload', 6], ['ldc_w.f32', 0.25], 'fsub', ['fload', 6], ['ldc_w.f32', 0.25], 'fsub', ['fload', 6], ['ldc_w.f32', 0.25], 'fsub'),
		*_fn_vertex(15.0, 0.0, 13.0, 15.0, 16.0),
		*_fn_vertex(1.0, 0.0, 13.0, 1.0, 16.0),

		*_texture_override(183, 'skip_west_1_smooth'),

		*_fn_set_tessellator_color(['fload', 6], ['fload', 6], ['fload', 6]),
		*_fn_vertex(1.0, 6.0, 15.0, 1.0, 10.0),
		*_fn_set_tessellator_color(['fload', 6], ['ldc_w.f32', 0.25], 'fsub', ['fload', 6], ['ldc_w.f32', 0.25], 'fsub', ['fload', 6], ['ldc_w.f32', 0.25], 'fsub'),
		*_fn_vertex(1.0, 0.0, 15.0, 1.0, 16.0),
		*_fn_vertex(15.0, 0.0, 15.0, 15.0, 16.0),
		*_fn_set_tessellator_color(['fload', 6], ['fload', 6], ['fload', 6]),
		*_fn_vertex(15.0, 6.0, 15.0, 15.0, 10.0),

		*_texture_override(183, 'skip_west_2_smooth'),

		*_fn_set_tessellator_color(['fload', 6], ['fload', 6], ['fload', 6]),
		*_fn_vertex(1.0, 6.0, 3.0, 1.0, 10.0),
		*_fn_set_tessellator_color(['fload', 6], ['ldc_w.f32', 0.25], 'fsub', ['fload', 6], ['ldc_w.f32', 0.25], 'fsub', ['fload', 6], ['ldc_w.f32', 0.25], 'fsub'),
		*_fn_vertex(1.0, 0.0, 3.0, 1.0, 16.0),
		*_fn_vertex(15.0, 0.0, 3.0, 15.0, 16.0),
		*_fn_set_tessellator_color(['fload', 6], ['fload', 6], ['fload', 6]),
		*_fn_vertex(15.0, 6.0, 3.0, 15.0, 10.0),

		['iload', 10],
		'iconst_1',
		['if_icmpne', 'skip_render_seeds_filling_1_smooth'],
		*_texture_override(184, 'skip_seeds_filling_1_smooth'),
		*_fn_set_tessellator_color(['fload', 6], ['fload', 6], ['fload', 6]),
		*_fn_vertex(3.0, 3.0, 3.0, 3.0, 3.0),
		*_fn_vertex(3.0, 3.0, 13.0, 3.0, 13.0),
		*_fn_vertex(13.0, 3.0, 13.0, 13.0, 13.0),
		*_fn_vertex(13.0, 3.0, 3.0, 13.0, 3.0),
		['label', 'skip_render_seeds_filling_1_smooth'],

		['iload', 10],
		'iconst_2',
		['if_icmpne', 'skip_render_seeds_filling_2_smooth'],
		*_texture_override(184, 'skip_seeds_filling_2_smooth'),
		*_fn_set_tessellator_color(['fload', 6], ['fload', 6], ['fload', 6]),
		*_fn_vertex(3.0, 4.0, 3.0, 3.0, 3.0),
		*_fn_vertex(3.0, 4.0, 13.0, 3.0, 13.0),
		*_fn_vertex(13.0, 4.0, 13.0, 13.0, 13.0),
		*_fn_vertex(13.0, 4.0, 3.0, 13.0, 3.0),
		['label', 'skip_render_seeds_filling_2_smooth'],

		['iload', 10],
		'iconst_3',
		['if_icmpne', 'skip_render_seeds_filling_3_smooth'],
		*_texture_override(184, 'skip_seeds_filling_3_smooth'),
		*_fn_set_tessellator_color(['fload', 6], ['fload', 6], ['fload', 6]),
		*_fn_vertex(3.0, 5.0, 3.0, 3.0, 3.0),
		*_fn_vertex(3.0, 5.0, 13.0, 3.0, 13.0),
		*_fn_vertex(13.0, 5.0, 13.0, 13.0, 13.0),
		*_fn_vertex(13.0, 5.0, 3.0, 13.0, 3.0),
		['label', 'skip_render_seeds_filling_3_smooth'],

		['goto', 'skip_else_block'],

		['label', 'skip_smooth_rendering'],

		['aload', 5], ['fload', 6], ['fload', 6], ['fload', 6],
		['invokevirtual', 'nw', 'a', '(FFF)V'],

		*_texture_override(180, 'skip_1'),

		*_fn_vertex(1.0, 6.0, 1.0, 1.0, 1.0),
		*_fn_vertex(1.0, 6.0, 15.0, 1.0, 15.0),
		*_fn_vertex(15.0, 6.0, 15.0, 15.0, 15.0),
		*_fn_vertex(15.0, 6.0, 1.0, 15.0, 1.0),

		*_texture_override(181, 'skip_2'),

		*_fn_vertex(3.0, 2.0, 3.0, 3.0, 3.0),
		*_fn_vertex(3.0, 2.0, 13.0, 3.0, 13.0),
		*_fn_vertex(13.0, 2.0, 13.0, 13.0, 13.0),
		*_fn_vertex(13.0, 2.0, 3.0, 13.0, 3.0),

		*_texture_override(182, 'skip_bottom'),

		*_fn_vertex(1.0, 0.0, 15.0, 1.0, 15.0),
		*_fn_vertex(1.0, 0.0, 1.0, 1.0, 1.0),
		*_fn_vertex(15.0, 0.0, 1.0, 15.0, 1.0),
		*_fn_vertex(15.0, 0.0, 15.0, 15.0, 15.0),

		*_texture_override(183, 'skip_north_1'),

		*_fn_vertex(1.0, 6.0, 15.0, 15.0, 10.0),
		*_fn_vertex(1.0, 6.0, 1.0, 1.0, 10.0),
		*_fn_vertex(1.0, 0.0, 1.0, 1.0, 16.0),
		*_fn_vertex(1.0, 0.0, 15.0, 15.0, 16.0),

		*_texture_override(183, 'skip_north_2'),

		*_fn_vertex(13.0, 6.0, 15.0, 15.0, 10.0),
		*_fn_vertex(13.0, 6.0, 1.0, 1.0, 10.0),
		*_fn_vertex(13.0, 0.0, 1.0, 1.0, 16.0),
		*_fn_vertex(13.0, 0.0, 15.0, 15.0, 16.0),

		*_texture_override(183, 'skip_south_1'),

		*_fn_vertex(15.0, 0.0, 15.0, 15.0, 16.0),
		*_fn_vertex(15.0, 0.0, 1.0, 1.0, 16.0),
		*_fn_vertex(15.0, 6.0, 1.0, 1.0, 10.0),
		*_fn_vertex(15.0, 6.0, 15.0, 15.0, 10.0),

		*_texture_override(183, 'skip_south_2'),

		*_fn_vertex(3.0, 0.0, 15.0, 15.0, 16.0),
		*_fn_vertex(3.0, 0.0, 1.0, 1.0, 16.0),
		*_fn_vertex(3.0, 6.0, 1.0, 1.0, 10.0),
		*_fn_vertex(3.0, 6.0, 15.0, 15.0, 10.0),

		*_texture_override(183, 'skip_east_1'),

		*_fn_vertex(1.0, 6.0, 1.0, 1.0, 10.0),
		*_fn_vertex(15.0, 6.0, 1.0, 15.0, 10.0),
		*_fn_vertex(15.0, 0.0, 1.0, 15.0, 16.0),
		*_fn_vertex(1.0, 0.0, 1.0, 1.0, 16.0),

		*_texture_override(183, 'skip_east_2'),

		*_fn_vertex(1.0, 6.0, 13.0, 1.0, 10.0),
		*_fn_vertex(15.0, 6.0, 13.0, 15.0, 10.0),
		*_fn_vertex(15.0, 0.0, 13.0, 15.0, 16.0),
		*_fn_vertex(1.0, 0.0, 13.0, 1.0, 16.0),

		*_texture_override(183, 'skip_west_1'),

		*_fn_vertex(1.0, 6.0, 15.0, 1.0, 10.0),
		*_fn_vertex(1.0, 0.0, 15.0, 1.0, 16.0),
		*_fn_vertex(15.0, 0.0, 15.0, 15.0, 16.0),
		*_fn_vertex(15.0, 6.0, 15.0, 15.0, 10.0),

		*_texture_override(183, 'skip_west_2'),

		*_fn_vertex(1.0, 6.0, 3.0, 1.0, 10.0),
		*_fn_vertex(1.0, 0.0, 3.0, 1.0, 16.0),
		*_fn_vertex(15.0, 0.0, 3.0, 15.0, 16.0),
		*_fn_vertex(15.0, 6.0, 3.0, 15.0, 10.0),

		['iload', 10],
		'iconst_1',
		['if_icmpne', 'skip_render_seeds_filling_1'],
		*_texture_override(184, 'skip_seeds_filling_1'),
		*_fn_set_tessellator_color(['fload', 6], ['fload', 6], ['fload', 6]),
		*_fn_vertex(3.0, 3.0, 3.0, 3.0, 3.0),
		*_fn_vertex(3.0, 3.0, 13.0, 3.0, 13.0),
		*_fn_vertex(13.0, 3.0, 13.0, 13.0, 13.0),
		*_fn_vertex(13.0, 3.0, 3.0, 13.0, 3.0),
		['label', 'skip_render_seeds_filling_1'],

		['iload', 10],
		'iconst_2',
		['if_icmpne', 'skip_render_seeds_filling_2'],
		*_texture_override(184, 'skip_seeds_filling_2'),
		*_fn_set_tessellator_color(['fload', 6], ['fload', 6], ['fload', 6]),
		*_fn_vertex(3.0, 4.0, 3.0, 3.0, 3.0),
		*_fn_vertex(3.0, 4.0, 13.0, 3.0, 13.0),
		*_fn_vertex(13.0, 4.0, 13.0, 13.0, 13.0),
		*_fn_vertex(13.0, 4.0, 3.0, 13.0, 3.0),
		['label', 'skip_render_seeds_filling_2'],

		['iload', 10],
		'iconst_3',
		['if_icmpne', 'skip_render_seeds_filling_3'],
		*_texture_override(184, 'skip_seeds_filling_3'),
		*_fn_set_tessellator_color(['fload', 6], ['fload', 6], ['fload', 6]),
		*_fn_vertex(3.0, 5.0, 3.0, 3.0, 3.0),
		*_fn_vertex(3.0, 5.0, 13.0, 3.0, 13.0),
		*_fn_vertex(13.0, 5.0, 13.0, 13.0, 13.0),
		*_fn_vertex(13.0, 5.0, 3.0, 13.0, 3.0),
		['label', 'skip_render_seeds_filling_3'],

		['label', 'skip_else_block'],

		'iconst_1',
		'ireturn'
	]

	code = assemble_code(cf, cp_cache, 0, 0, code)
	a_code = a_code_assemble([
		(13).to_bytes(2),
		(11).to_bytes(2),
		len(code).to_bytes(4),
		code,
		(0).to_bytes(2),
		[],
		(0).to_bytes(2),
		[]
	])

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [[i2cpx_utf8(cf, cp_cache, 'Code'), len(a_code).to_bytes(4), a_code]]

	return m
