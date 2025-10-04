package com.thebluetropics.crabpack;

public final class Zoom {
	public static float current = 1.0f;
	public static float defaultTarget = 1.0f;
	public static float zoomTarget = 2.0f;
	public static float[] presets = new float[] { 2.0f, 4.0f, 8.0f, 16.0f, 32.0f, 64.0f };
	public static int index = 0;
	public static boolean zooming = false;

	public static void onKey(boolean isKeyDown) {
		if (isKeyDown) {
			zooming = true;
			zoomTarget = 2.0f;
			index = 0;
		} else {
			zooming = false;
		}
	}

	public static boolean onMouseScroll(int dir) {
		if (zooming) {
			if (dir > 0) {
				if (index < (presets.length - 1)) {
					index = index + 1;
					zoomTarget = presets[index];
				}
			}

			if (dir < 0) {
				if (index > 0) {
					index = index - 1;
					zoomTarget = presets[index];
				}
			}

			return true;
		}

		return false;
	}

	public static float onRenderBegin(float tickDelta) {
		if (zooming) {
			current = current + (zoomTarget - current) * 0.15f;
		} else {
			current = current + (defaultTarget - current) * 0.15f;
		}

		if (Math.abs(current - defaultTarget) < 0.01) {
			return 1.0f;
		}

		return current;
	}
}
