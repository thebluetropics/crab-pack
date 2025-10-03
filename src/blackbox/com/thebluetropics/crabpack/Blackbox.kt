package com.thebluetropics.crabpack

import java.io.BufferedOutputStream
import java.io.File
import java.io.FileOutputStream
import java.nio.ByteBuffer
import java.nio.ByteOrder
import java.nio.file.Path
import java.time.LocalDateTime

object Blackbox {
	private val states = mutableMapOf<String, State>()
	private var dir: Path? = null
	private var active: Boolean = false

	fun startClient(file: File) {
		if (!this.active) {
			this.dir = file.parentFile.toPath()
			this.active = true
			println("Blackbox started.")
		}
	}

	fun stopClient() {
		if (this.active) {
			this.active = false

			for (player in this.states.keys) {
				this.stopPlayerSession(player)
			}

			println("Blackbox stopped.")
		}
	}

	fun startServer() {
		if (!this.active) {
			this.active = true
			val file = File("blackbox")
			if (!file.exists()) {
				file.mkdir()
			}
			this.dir = file.toPath()
			println("Blackbox started.")
		}
	}

	fun stopServer() {
		if (this.active) {
			this.active = false

			for (player in this.states.keys) {
				this.stopPlayerSession(player)
			}

			println("Blackbox stopped.")
		}
	}

	fun onPlayerTick(
		player: String,
		dim: Int,
		x: Double,
		y: Double,
		z: Double,
		yaw: Float,
		pitch: Float,
		sneaking: Boolean
	) {
		if (this.active) {
			val dim = if (dim.equals(-1)) "nether" else "overworld"

			if (!this.states.contains(player)) {
				this.startPlayerSession(player, dim)
			}

			var state = this.states[player] as State

			if (dim != state.dim) {
				this.stopPlayerSession(player)
				this.startPlayerSession(player, dim)
				state = this.states[player] as State
			}

			val now = System.nanoTime()
			val elapsed = now - state.lastSnapshot

			if (elapsed >= 500000000) {
				state.lastSnapshot = now

				val buf = ByteBuffer.allocate(38).order(ByteOrder.LITTLE_ENDIAN)
				buf.putInt(((now - state.t) / 1000000).toInt())

				buf.put(0) // → Entry type `snapshot`

				buf.putDouble(x)
				buf.putDouble(y)
				buf.putDouble(z)

				var yaw = yaw % 360 // 0.0 or 360.0 → +Z, 180.0 → -Z, +X? -X?
				if (yaw < 0) {
					yaw += 360
				}
				buf.putFloat(yaw)
				val pitch = Math.max(-1.0f, Math.min(1.0f, -pitch / 90.0f)) // 0.0 → Forward, 1.0 → Up, -1.0 → Down
				buf.putFloat(pitch)

				buf.put(if (sneaking) 1 else 0)

				state.stream.write(buf.array())
			}
		}
	}

	private fun startPlayerSession(player: String, dim: String) {
		val date = LocalDateTime.now()

		val filename = "${player}_${date.year}${String.format("%02d", date.monthValue)}${String.format("%02d", date.dayOfMonth)}${String.format("%02d", date.hour)}${String.format("%02d", date.minute)}${String.format("%02d", date.second)}.blackbox"
		val file = (this.dir as Path).resolve(filename).toFile()
		val state = State(BufferedOutputStream(FileOutputStream(file), 32 * 1024), dim, System.nanoTime(), System.nanoTime())

		state.stream.write(ByteBuffer.allocate(2).order(ByteOrder.LITTLE_ENDIAN).putShort(2).array())
		state.stream.write(player.length.and(255))
		state.stream.write(player.toByteArray(Charsets.UTF_8))

		var timestamp: Long = 0
		timestamp = timestamp or ((date.year.toLong() and ((1 shl 20) - 1)) shl 28)
		timestamp = timestamp or (((date.monthValue - 1).toLong() and 0x1f) shl 23)
		timestamp = timestamp or (((date.dayOfMonth - 1).toLong() and 0x3f) shl 17)
		timestamp = timestamp or ((date.hour.toLong() and 0x1f) shl 12)
		timestamp = timestamp or ((date.minute.toLong() and 0x3f) shl 6)
		timestamp = timestamp or (date.second.toLong() and 0x3f)

		val timestampBytes = ByteArray(6, fun(i: Int): Byte {
			return ((timestamp shr (i * 8)) and 0xff).toByte()
		})

		state.stream.write(timestampBytes)
		state.stream.write(ByteBuffer.allocate(4).order(ByteOrder.LITTLE_ENDIAN).putInt(date.nano).array())
		state.stream.write(if (dim.equals("overworld")) 0 else 1)

		this.states[player] = state

		println("Started recording for player ${player}.")
	}

	private fun stopPlayerSession(player: String) {
		val state = this.states[player] as State
		state.stream.close()
		this.states.remove(player)

		println("Stopped recording for player ${player}.")
	}

	fun onPlayerDied(player: String) {
		if (this.active) {
			if (this.states.contains(player)) {
				println("Player ${player} died, stop recording for this player.")
				stopPlayerSession(player)
			}
		}
	}

	fun onPlayerLeft(player: String) {
		if (this.active) {
			if (this.states.contains(player)) {
				println("Player ${player} left, stop recording for this player.")
				stopPlayerSession(player)
			}
		}
	}

	fun onBreakBlock(player: String, x: Int, y: Int, z: Int) {
		if (this.active) {
			if (this.states.contains(player)) {
				val state = this.states[player] as State

				val buf = ByteBuffer.allocate(17).order(ByteOrder.LITTLE_ENDIAN)
				buf.putInt(((System.nanoTime() - state.t) / 1000000).toInt())
				buf.put(1)

				buf.putInt(x)
				buf.putInt(y)
				buf.putInt(z)

				state.stream.write(buf.array())
			}
		}
	}

	fun onPlaceBlock(player: String, x: Int, y: Int, z: Int, block: Int, meta: Int) {
		if (this.active) {
			if (this.states.contains(player)) {
				val state = this.states[player] as State

				val buf = ByteBuffer.allocate(19).order(ByteOrder.LITTLE_ENDIAN)
				buf.putInt(((System.nanoTime() - state.t) / 1000000).toInt())
				buf.put(2)

				buf.putInt(x)
				buf.putInt(y)
				buf.putInt(z)

				buf.put(block.toByte())
				buf.put(meta.toByte())

				state.stream.write(buf.array())
			}
		}
	}
}
