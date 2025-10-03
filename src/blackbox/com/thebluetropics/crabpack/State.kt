package com.thebluetropics.crabpack

import java.io.BufferedOutputStream
import java.io.File

class State(val stream: BufferedOutputStream, val dim: String, val t: Long, var lastSnapshot: Long) {
}
