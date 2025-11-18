package main

import (
	"fmt"
	"log"
	"math"
	"math/rand"
	"runtime"
	"time"

	"github.com/go-gl/gl/v4.1-core/gl"
	"github.com/go-gl/glfw/v3.3/glfw"
	"github.com/go-gl/mathgl/mgl32"
)

const (
	windowWidth  = 800
	windowHeight = 600
)

type Player struct {
	Pos              mgl32.Vec3
	Yaw, Pitch       float32
	Height           float32
	Speed            float32
	MouseSensitivity float32
}

type Cube struct {
	Pos  mgl32.Vec3
	Size float32
	Col  mgl32.Vec3
}

var cubes []Cube

func init() {
	// GLFW event handling must run on the main OS thread
	runtime.LockOSThread()
}

func initGlfw() *glfw.Window {
	if err := glfw.Init(); err != nil {
		log.Fatalln("failed to initialize glfw:", err)
	}
	glfw.WindowHint(glfw.ContextVersionMajor, 3)
	glfw.WindowHint(glfw.ContextVersionMinor, 3)
	glfw.WindowHint(glfw.OpenGLProfile, glfw.OpenGLCoreProfile)
	glfw.WindowHint(glfw.OpenGLForwardCompatible, glfw.True)

	window, err := glfw.CreateWindow(windowWidth, windowHeight, "Walking Around (Go)", nil, nil)
	if err != nil {
		log.Fatalln("failed to create window:", err)
	}
	window.MakeContextCurrent()
	window.SetInputMode(glfw.CursorMode, glfw.CursorDisabled)
	return window
}

func initOpenGL() {
	if err := gl.Init(); err != nil {
		log.Fatalln("failed to initialize glow:", err)
	}
	version := gl.GoStr(gl.GetString(gl.VERSION))
	fmt.Println("OpenGL version", version)
	gl.Enable(gl.DEPTH_TEST)
}

// Simple vertex and fragment shaders with color uniform and MVP matrix
var vertexShader = `#version 330 core
layout(location = 0) in vec3 vp;
uniform mat4 mvp;
void main() {
	gl_Position = mvp * vec4(vp, 1.0);
}
`

var fragmentShader = `#version 330 core
out vec4 fragColor;
uniform vec3 uColor;
void main() {
	fragColor = vec4(uColor, 1.0);
}
`

func compileShader(src string, shaderType uint32) (uint32, error) {
	shader := gl.CreateShader(shaderType)
	csources, free := gl.Strs(src + "\x00")
	defer free()
	gl.ShaderSource(shader, 1, csources, nil)
	gl.CompileShader(shader)

	var status int32
	gl.GetShaderiv(shader, gl.COMPILE_STATUS, &status)
	if status == gl.FALSE {
		var logLength int32
		gl.GetShaderiv(shader, gl.INFO_LOG_LENGTH, &logLength)
		log := make([]byte, logLength+1)
		gl.GetShaderInfoLog(shader, logLength, nil, &log[0])
		return 0, fmt.Errorf("failed to compile shader: %s", string(log))
	}
	return shader, nil
}

func newProgram(vertexSrc, fragmentSrc string) (uint32, error) {
	vs, err := compileShader(vertexSrc, gl.VERTEX_SHADER)
	if err != nil {
		return 0, err
	}
	fs, err := compileShader(fragmentSrc, gl.FRAGMENT_SHADER)
	if err != nil {
		return 0, err
	}
	prog := gl.CreateProgram()
	gl.AttachShader(prog, vs)
	gl.AttachShader(prog, fs)
	gl.LinkProgram(prog)

	var status int32
	gl.GetProgramiv(prog, gl.LINK_STATUS, &status)
	if status == gl.FALSE {
		var logLength int32
		gl.GetProgramiv(prog, gl.INFO_LOG_LENGTH, &logLength)
		log := make([]byte, logLength+1)
		gl.GetProgramInfoLog(prog, logLength, nil, &log[0])
		return 0, fmt.Errorf("failed to link program: %s", string(log))
	}
	gl.DeleteShader(vs)
	gl.DeleteShader(fs)
	return prog, nil
}

func makeCubeVao() (uint32, int) {
	// 36 vertices (6 faces * 2 tris * 3 verts)
	vertices := []float32{
		// front
		-1, -1, 1,
		1, -1, 1,
		1, 1, 1,
		1, 1, 1,
		-1, 1, 1,
		-1, -1, 1,
		// back
		-1, -1, -1,
		-1, 1, -1,
		1, 1, -1,
		1, 1, -1,
		1, -1, -1,
		-1, -1, -1,
		// left
		-1, -1, -1,
		-1, -1, 1,
		-1, 1, 1,
		-1, 1, 1,
		-1, 1, -1,
		-1, -1, -1,
		// right
		1, -1, -1,
		1, 1, -1,
		1, 1, 1,
		1, 1, 1,
		1, -1, 1,
		1, -1, -1,
		// top
		-1, 1, -1,
		-1, 1, 1,
		1, 1, 1,
		1, 1, 1,
		1, 1, -1,
		-1, 1, -1,
		// bottom
		-1, -1, -1,
		1, -1, -1,
		1, -1, 1,
		1, -1, 1,
		-1, -1, 1,
		-1, -1, -1,
	}

	var vao uint32
	var vbo uint32
	gl.GenVertexArrays(1, &vao)
	gl.GenBuffers(1, &vbo)

	gl.BindVertexArray(vao)
	gl.BindBuffer(gl.ARRAY_BUFFER, vbo)
	gl.BufferData(gl.ARRAY_BUFFER, 4*len(vertices), gl.Ptr(vertices), gl.STATIC_DRAW)
	gl.EnableVertexAttribArray(0)
	gl.VertexAttribPointer(0, 3, gl.FLOAT, false, 0, gl.PtrOffset(0))

	gl.BindBuffer(gl.ARRAY_BUFFER, 0)
	gl.BindVertexArray(0)
	return vao, len(vertices) / 3
}

func main() {
	rand.Seed(time.Now().UnixNano())
	window := initGlfw()
	defer glfw.Terminate()
	initOpenGL()

	prog, err := newProgram(vertexShader, fragmentShader)
	if err != nil {
		log.Fatalln(err)
	}
	vao, vertCount := makeCubeVao()

	// create some cubes (4 in a circle like original)
	for i := 1; i <= 4; i++ {
		posI := float64(i) * (2 * math.Pi) / 4.0
		xPos := float32(math.Cos(posI) * 10.0)
		yPos := float32(math.Sin(posI) * 10.0)
		x := rand.Float32()*200 - 100
		y := rand.Float32()*200 - 100
		z := rand.Float32()*200 - 100
		denom := x + y + z
		if denom == 0 {
			denom = 1
		}
		color := mgl32.Vec3{float32(x) / float32(denom), float32(y) / float32(denom), float32(z) / float32(denom)}
		cubes = append(cubes, Cube{Pos: mgl32.Vec3{xPos, yPos, 0}, Size: 0.9, Col: color})
	}

	player := Player{
		Pos:              mgl32.Vec3{0, 0, 0},
		Yaw:              0,
		Pitch:            0,
		Height:           1.6,
		Speed:            6.0,
		MouseSensitivity: 0.15,
	}

	proj := mgl32.Perspective(mgl32.DegToRad(45.0), float32(windowWidth)/float32(windowHeight), 0.1, 280.0)

	// timing
	lastTime := time.Now()
	fpsTimer := time.Now()
	frames := 0

	// cursor tracking
	var lastX, lastY float64
	lastX = float64(windowWidth) / 2
	lastY = float64(windowHeight) / 2
	window.SetCursorPos(lastX, lastY)

	gl.UseProgram(prog)
	mvpLoc := gl.GetUniformLocation(prog, gl.Str("mvp\x00"))
	colorLoc := gl.GetUniformLocation(prog, gl.Str("uColor\x00"))

	for !window.ShouldClose() {
		// time
		now := time.Now()
		dt := float32(now.Sub(lastTime).Seconds())
		lastTime = now

		// input
		glfw.PollEvents()

		x, y := window.GetCursorPos()
		dx := float32(x - lastX)
		dy := float32(y - lastY)
		lastX = x
		lastY = y

		player.Yaw += dx * player.MouseSensitivity * dt * 60
		player.Pitch -= dy * player.MouseSensitivity * dt * 60
		// clamp pitch
		if player.Pitch > 89.0 {
			player.Pitch = 89.0
		}
		if player.Pitch < -89.0 {
			player.Pitch = -89.0
		}

		// movement
		dir := mgl32.Vec3{0, 0, 0}
		if window.GetKey(glfw.KeyW) == glfw.Press {
			dir = dir.Add(mgl32.Vec3{0, 0, -1})
		}
		if window.GetKey(glfw.KeyS) == glfw.Press {
			dir = dir.Add(mgl32.Vec3{0, 0, 1})
		}
		if window.GetKey(glfw.KeyA) == glfw.Press {
			dir = dir.Add(mgl32.Vec3{-1, 0, 0})
		}
		if window.GetKey(glfw.KeyD) == glfw.Press {
			dir = dir.Add(mgl32.Vec3{1, 0, 0})
		}
		if window.GetKey(glfw.KeySpace) == glfw.Press {
			// spawn a random cube like original
			x := rand.Float32()*200 - 100
			y := rand.Float32()*200 - 100
			z := rand.Float32()*200 - 100
			denom := x + y + z
			if denom == 0 {
				denom = 1
			}
			color := mgl32.Vec3{x / denom, y / denom, z / denom}
			cubes = append(cubes, Cube{Pos: mgl32.Vec3{x, y, z}, Size: rand.Float32()*2.25 + 0.25, Col: color})
		}

		// build forward/right vectors from yaw/pitch
		yawRad := mgl32.DegToRad(player.Yaw)
		front := mgl32.Vec3{float32(math.Cos(float64(yawRad))), 0, float32(math.Sin(float64(yawRad)))}
		right := front.Cross(mgl32.Vec3{0, 1, 0}).Normalize()

		if dir.Len() > 0 {
			move := mgl32.Vec3{0, 0, 0}
			move = move.Add(front.Mul(dir.Z()))
			move = move.Add(right.Mul(dir.X()))
			move = move.Normalize().Mul(player.Speed * dt)
			player.Pos = player.Pos.Add(move)
		}

		// camera
		eye := player.Pos.Add(mgl32.Vec3{0, player.Height, 0})
		// use yaw and pitch to compute forward direction
		yaw := mgl32.DegToRad(player.Yaw)
		pitch := mgl32.DegToRad(player.Pitch)
		fx := float32(math.Cos(float64(yaw)) * math.Cos(float64(pitch)))
		fy := float32(math.Sin(float64(pitch)))
		fz := float32(math.Sin(float64(yaw)) * math.Cos(float64(pitch)))
		forward := mgl32.Vec3{fx, fy, fz}.Normalize()
		center := eye.Add(forward)
		view := mgl32.LookAtV(eye, center, mgl32.Vec3{0, 1, 0})

		// render
		gl.ClearColor(0.1, 0.1, 0.1, 1.0)
		gl.Clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT)

		gl.BindVertexArray(vao)
		for _, c := range cubes {
			model := mgl32.Translate3D(c.Pos.X(), c.Pos.Y(), c.Pos.Z()).Mul4(mgl32.Scale3D(c.Size, c.Size, c.Size))
			mvp := proj.Mul4(view).Mul4(model)
			gl.UniformMatrix4fv(mvpLoc, 1, false, &mvp[0])
			gl.Uniform3f(colorLoc, c.Col.X(), c.Col.Y(), c.Col.Z())
			gl.DrawArrays(gl.TRIANGLES, 0, int32(vertCount))
		}
		gl.BindVertexArray(0)

		window.SwapBuffers()

		frames++
		if time.Since(fpsTimer) >= time.Second {
			fps := frames
			window.SetTitle(fmt.Sprintf("Walking Around (Go) - FPS: %d - Cubes: %d", fps, len(cubes)))
			frames = 0
			fpsTimer = time.Now()
		}
	}
}
