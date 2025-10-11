package com.thebluetropics.crabpack;

import org.lwjgl.opengl.GL11;

import java.lang.invoke.MethodHandle;
import java.lang.invoke.MethodHandles;
import java.lang.invoke.MethodType;

public class MinimalCrosshair {
	private static final MethodHandle getTessellator;
	private static final MethodHandle startQuads;
	private static final MethodHandle vertex;
	private static final MethodHandle draw;

	public static int scaleFactor = 1;
	public static int scaledWidth = 0;
	public static int scaledHeight = 0;

	public static void beforeRenderCrosshair(int pScaleFactor, int pScaledWidth, int pScaledHeight) {
		scaleFactor = pScaleFactor;
		scaledWidth = pScaledWidth;
		scaledHeight = pScaledHeight;
	}

	public static void renderCrosshair() {
		try {
			Object tessellator = getTessellator.invoke();
			GL11.glDisable(3553);
			GL11.glColor4f(1.0f, 1.0f, 1.0f, 1.0f);
			startQuads.invoke(tessellator);
			double crosshairSize = 2.0 / ((double) scaleFactor);
			double x = (((double) scaledWidth) / 2.0) - (crosshairSize / 2.0);
			double y = (((double) scaledHeight) / 2.0) - (crosshairSize / 2.0);
			vertex.invoke(tessellator, x, y + crosshairSize, 0.0);
			vertex.invoke(tessellator, x + crosshairSize, y + crosshairSize, 0.0);
			vertex.invoke(tessellator, x + crosshairSize, y, 0.0);
			vertex.invoke(tessellator, x, y, 0.0);
			draw.invoke(tessellator);
			GL11.glEnable(3553);
		} catch(Throwable e) {
			e.printStackTrace();
		}
	}

	static {
		try {
			MethodHandles.Lookup lookup = MethodHandles.lookup();
			getTessellator = lookup.findStaticGetter(Class.forName("nw"), "a", Class.forName("nw"));
			startQuads = lookup.findVirtual(Class.forName("nw"), "b", MethodType.methodType(void.class));
			vertex = lookup.findVirtual(Class.forName("nw"), "a", MethodType.methodType(void.class, double.class, double.class, double.class));
			draw = lookup.findVirtual(Class.forName("nw"), "a", MethodType.methodType(void.class));
		} catch(Exception e) {
			e.printStackTrace();
			throw new RuntimeException();
		}
	}
}
