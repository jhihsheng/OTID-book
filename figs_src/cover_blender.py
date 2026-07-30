"""OTID course-cover v3 — "holographic landscape x photonic chip" (bpy / Cycles).

Art direction (per 老師 2026-07-30): deep-navy tech scene. A glowing holographic
contour landscape (the optimization design space) floats above a photonic chip;
a gold trajectory climbs past a local maximum (SA hop, QA tunnel through the
translucent holo-hill) to the global maximum, where a refined chibi of 老師
(modeled on the dop.nycu.edu.tw portrait: swept bangs, rectangular glasses, navy
suit, dusty-pink tie) plants the ∇f = 0 flag. On the chip: a topology-optimized
waveguide bend with light routed through, a 1D grating with diffracted beams,
and an Ising spin array — the course's three inverse-design threads.

Run:     python3 figs_src/cover_blender.py [--preview] [--closeup]
Output:  scratchpad cover_render.png (3200x2000; --preview 800x500 low samples)
"""
import math
import sys

import bpy
from mathutils import Vector

OUT = "/tmp/claude-1000/-home-jwu-OTID-book/689a37ca-f036-4c23-b387-17c9e73f49ab/scratchpad/cover_render.png"
PREVIEW = "--preview" in sys.argv
DRAFT = "--draft" in sys.argv
CLOSEUP = "--closeup" in sys.argv

# ---------------------------------------------------------------- palette
def srgb(hexstr, alpha=1.0):
    h = hexstr.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    lin = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return (*lin, alpha)

CYAN   = srgb("#46e6ff")
CYAN2  = srgb("#7af0ff")
GOLD   = srgb("#ffc76a")
ROSE   = srgb("#ff5f7e")
NAVY   = srgb("#232b3d")
INK    = srgb("#1a1d22")
SKIN   = srgb("#fac192")
IVORY  = srgb("#fff7ea")
TIE    = srgb("#c9849c")

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# ---------------------------------------------------------------- helpers
def g(x, y, sx, sy):
    return math.exp(-(x * x / (2 * sx * sx) + y * y / (2 * sy * sy)))

HOLO_Z = 1.5    # hologram floats this far above the chip
HX0, HX1, HY0, HY1 = -6.5, 7.5, -1.8, 6.2   # hologram footprint

def edge_fade(x, y):
    """Taper the hologram to its base plane at the panel borders."""
    def s(t):
        t = max(0.0, min(1.0, t))
        return t * t * (3 - 2 * t)
    return (s((x - HX0) / 1.2) * s((HX1 - x) / 1.2) *
            s((y - HY0) / 1.2) * s((HY1 - y) / 1.2))

def height(x, y):
    """Design-space landscape (relative to hologram base plane)."""
    z = 0.15
    z += 2.55 * g(x - 2.6, y - 0.6, 1.50, 1.30)      # global maximum
    z += 1.80 * g(x + 2.4, y - 0.1, 1.25, 1.10)      # local maximum
    z += 0.40 * g(x + 6.0, y - 1.0, 2.0, 1.6)
    z += 0.10 * math.sin(1.1 * x) * math.cos(0.9 * y)
    z += 0.04 * math.sin(2.3 * x + 0.8) * math.sin(1.7 * y + 0.3)
    return z * edge_fade(x, y)

def make_mesh(name, verts, faces, mat):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    for p in mesh.polygons:
        p.use_smooth = True
    ob = bpy.data.objects.new(name, mesh)
    ob.data.materials.append(mat)
    scene.collection.objects.link(ob)
    return ob

def plain(name, color, rough=0.85, metallic=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    b = mat.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = color
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metallic
    return mat

def glow(name, color, strength):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = color
    em.inputs["Strength"].default_value = strength
    nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
    return mat

def add_sphere(loc, r, mat, name="s", scale=None, rot=None):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=48, ring_count=24)
    ob = bpy.context.object
    ob.name = name
    if scale:
        ob.scale = scale
    if rot:
        ob.rotation_euler = rot
    ob.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    return ob

def add_cyl(loc, r, depth, mat, rot=(0, 0, 0), name="c", vertices=32):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc, rotation=rot, vertices=vertices)
    ob = bpy.context.object
    ob.name = name
    ob.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    return ob

def add_box(loc, size, mat, rot=(0, 0, 0), name="b"):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    ob = bpy.context.object
    ob.name = name
    ob.scale = size
    ob.data.materials.append(mat)
    return ob

def add_capsule(p0, p1, r, mat, name="cap"):
    p0v, p1v = Vector(p0), Vector(p1)
    d = p1v - p0v
    mid = (p0v + p1v) / 2
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d.length, location=mid, vertices=32)
    ob = bpy.context.object
    ob.name = name
    ob.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
    ob.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    add_sphere(p0, r, mat, name + "_a")
    add_sphere(p1, r, mat, name + "_b")
    return ob

def tube_from_points(name, pts, radius, mat, bevel_res=8):
    curve = bpy.data.curves.new(name, type="CURVE")
    curve.dimensions = "3D"
    curve.bevel_depth = radius
    curve.bevel_resolution = bevel_res
    curve.use_fill_caps = True
    sp = curve.splines.new("NURBS")
    sp.points.add(len(pts) - 1)
    for p, (x, y, z) in zip(sp.points, pts):
        p.co = (x, y, z, 1)
    sp.use_endpoint_u = True
    ob = bpy.data.objects.new(name, curve)
    ob.data.materials.append(mat)
    scene.collection.objects.link(ob)
    return ob

# ---------------------------------------------------------------- photonic chip base
def chip_material():
    mat = bpy.data.materials.new("chip")
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Base Color"].default_value = srgb("#0a0e18")
    bsdf.inputs["Roughness"].default_value = 0.35
    bsdf.inputs["Metallic"].default_value = 0.6
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(geo.outputs["Position"], sep.inputs["Vector"])
    # sparse circuit traces: thin lines along x and y, masked by noise
    def band(axis_out):
        div = nt.nodes.new("ShaderNodeMath"); div.operation = "DIVIDE"
        div.inputs[1].default_value = 1.35
        nt.links.new(axis_out, div.inputs[0])
        fr = nt.nodes.new("ShaderNodeMath"); fr.operation = "FRACT"
        nt.links.new(div.outputs[0], fr.inputs[0])
        lt = nt.nodes.new("ShaderNodeMath"); lt.operation = "LESS_THAN"
        lt.inputs[1].default_value = 0.018
        nt.links.new(fr.outputs[0], lt.inputs[0])
        return lt
    bx = band(sep.outputs["X"])
    by = band(sep.outputs["Y"])
    mx = nt.nodes.new("ShaderNodeMath"); mx.operation = "MAXIMUM"
    nt.links.new(bx.outputs[0], mx.inputs[0])
    nt.links.new(by.outputs[0], mx.inputs[1])
    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 0.9
    gt = nt.nodes.new("ShaderNodeMath"); gt.operation = "GREATER_THAN"
    gt.inputs[1].default_value = 0.55
    nt.links.new(noise.outputs["Fac"], gt.inputs[0])
    mask = nt.nodes.new("ShaderNodeMath"); mask.operation = "MULTIPLY"
    nt.links.new(mx.outputs[0], mask.inputs[0])
    nt.links.new(gt.outputs[0], mask.inputs[1])
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = CYAN
    em.inputs["Strength"].default_value = 0.9
    add = nt.nodes.new("ShaderNodeAddShader")
    mixf = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(mask.outputs[0], mixf.inputs["Fac"])
    nt.links.new(bsdf.outputs["BSDF"], mixf.inputs[1])
    nt.links.new(bsdf.outputs["BSDF"], add.inputs[0])
    nt.links.new(em.outputs["Emission"], add.inputs[1])
    nt.links.new(add.outputs["Shader"], mixf.inputs[2])
    nt.links.new(mixf.outputs["Shader"], out.inputs["Surface"])
    return mat

add_box((0, 1.0, -0.06), (13.5, 13.0, 0.06), chip_material(), name="chip")

# ---------------------------------------------------------------- chip feature 1: TO waveguide bend (front-left)
to_cx, to_cy = -3.6, -3.1
add_box((to_cx, to_cy, 0.035), (1.25, 1.25, 0.035), plain("to_plate", srgb("#141b2b"), 0.5, 0.3), name="to_plate")
M_BLOB = plain("to_blob", srgb("#1f4b57"), 0.35)
try:
    b = M_BLOB.node_tree.nodes["Principled BSDF"]
    b.inputs["Emission Color"].default_value = srgb("#2fbcd6")
    b.inputs["Emission Strength"].default_value = 0.35
except KeyError:
    pass
blob_spots = [(-0.55, 0.42, 0.16, 0.11), (-0.15, 0.55, 0.13, 0.09), (0.35, 0.4, 0.19, 0.12),
              (0.72, 0.05, 0.14, 0.10), (-0.62, -0.05, 0.12, 0.09), (-0.2, 0.05, 0.2, 0.13),
              (0.3, -0.12, 0.12, 0.08), (-0.45, -0.5, 0.15, 0.10), (0.05, -0.55, 0.17, 0.11),
              (0.55, -0.52, 0.11, 0.08), (0.85, 0.55, 0.10, 0.07), (-0.85, 0.6, 0.11, 0.08)]
for k, (bx_, by_, br, bh) in enumerate(blob_spots):
    add_sphere((to_cx + bx_, to_cy + by_, 0.07 + bh * 0.35), br, M_BLOB,
               name=f"blob{k}", scale=(1.0, 0.85, bh / br))
M_WG = glow("waveguide", CYAN, 2.2)
add_box((to_cx - 1.95, to_cy + 0.42, 0.075), (0.75, 0.045, 0.02), M_WG, name="wg_in")
light_path = [(to_cx - 1.25, to_cy + 0.42, 0.085), (to_cx - 0.6, to_cy + 0.42, 0.09),
              (to_cx - 0.15, to_cy + 0.28, 0.10), (to_cx + 0.25, to_cy + 0.12, 0.10),
              (to_cx + 0.35, to_cy - 0.25, 0.10), (to_cx + 0.3, to_cy - 0.7, 0.09),
              (to_cx + 0.3, to_cy - 1.35, 0.085)]
tube_from_points("light_bend", light_path, 0.034, glow("light_bend_m", CYAN2, 6.0))
add_box((to_cx + 0.3, to_cy - 1.75, 0.075), (0.045, 0.75, 0.02), M_WG, name="wg_out")

# ---------------------------------------------------------------- chip feature 2: 1D grating + diffraction (front-right)
gr_cx, gr_cy = 4.3, -3.2
M_BAR = plain("grating_bar", srgb("#2a3a54"), 0.3, 0.7)
try:
    b = M_BAR.node_tree.nodes["Principled BSDF"]
    b.inputs["Emission Color"].default_value = srgb("#2fbcd6")
    b.inputs["Emission Strength"].default_value = 0.18
except KeyError:
    pass
for k in range(11):
    add_box((gr_cx - 0.8 + k * 0.16, gr_cy, 0.10), (0.032, 0.55, 0.10), M_BAR, name=f"grat{k}")
tube_from_points("gr_in", [(gr_cx - 1.9, gr_cy - 1.5, 1.25), (gr_cx - 0.15, gr_cy - 0.05, 0.22)],
                 0.024, glow("gr_in_m", GOLD, 3.5))
for k, (dx, dz) in enumerate([(-0.85, 1.15), (0.05, 1.45), (0.95, 1.15)]):
    tube_from_points(f"gr_out{k}", [(gr_cx, gr_cy, 0.22), (gr_cx + dx, gr_cy + 1.15, dz)],
                     0.016, glow(f"gr_out{k}_m", GOLD, 2.2))

# ---------------------------------------------------------------- chip feature 3: Ising spin array (mid-left)
sp_cx, sp_cy = -1.6, -4.4
M_PIN = plain("pin", srgb("#33415c"), 0.35, 0.6)
try:
    b = M_PIN.node_tree.nodes["Principled BSDF"]
    b.inputs["Emission Color"].default_value = srgb("#22364f")
    b.inputs["Emission Strength"].default_value = 0.25
except KeyError:
    pass
M_UP = glow("spin_up", GOLD, 2.5)
M_DN = glow("spin_dn", ROSE, 1.6)
updown = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1]
for j in range(5):
    for i in range(5):
        px, py = sp_cx + i * 0.42, sp_cy + j * 0.42
        up = updown[j * 5 + i]
        h = 0.16 if up else 0.08
        add_cyl((px, py, h / 2), 0.05, h, M_PIN, name=f"pin{i}_{j}", vertices=16)
        add_sphere((px, py, h + 0.035), 0.045, M_UP if up else M_DN, name=f"tip{i}_{j}")

# ---------------------------------------------------------------- holographic landscape
def holo_material():
    mat = bpy.data.materials.new("holo")
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(geo.outputs["Position"], sep.inputs["Vector"])
    # contour lines: bright cyan bands of constant z
    mul = nt.nodes.new("ShaderNodeMath"); mul.operation = "MULTIPLY"
    mul.inputs[1].default_value = 6.0
    nt.links.new(sep.outputs["Z"], mul.inputs[0])
    fr = nt.nodes.new("ShaderNodeMath"); fr.operation = "FRACT"
    nt.links.new(mul.outputs[0], fr.inputs[0])
    lt = nt.nodes.new("ShaderNodeMath"); lt.operation = "LESS_THAN"
    lt.inputs[1].default_value = 0.055
    nt.links.new(fr.outputs[0], lt.inputs[0])
    # sparse graph-paper grid in x and y
    def gridband(axis_out):
        dv = nt.nodes.new("ShaderNodeMath"); dv.operation = "DIVIDE"
        dv.inputs[1].default_value = 0.8
        nt.links.new(axis_out, dv.inputs[0])
        fr2 = nt.nodes.new("ShaderNodeMath"); fr2.operation = "FRACT"
        nt.links.new(dv.outputs[0], fr2.inputs[0])
        lt2 = nt.nodes.new("ShaderNodeMath"); lt2.operation = "LESS_THAN"
        lt2.inputs[1].default_value = 0.035
        nt.links.new(fr2.outputs[0], lt2.inputs[0])
        return lt2
    gx = gridband(sep.outputs["X"])
    gy = gridband(sep.outputs["Y"])
    gmax = nt.nodes.new("ShaderNodeMath"); gmax.operation = "MAXIMUM"
    nt.links.new(gx.outputs[0], gmax.inputs[0])
    nt.links.new(gy.outputs[0], gmax.inputs[1])
    gdim = nt.nodes.new("ShaderNodeMath"); gdim.operation = "MULTIPLY"
    gdim.inputs[1].default_value = 0.45
    nt.links.new(gmax.outputs[0], gdim.inputs[0])
    combined = nt.nodes.new("ShaderNodeMath"); combined.operation = "MAXIMUM"
    nt.links.new(lt.outputs[0], combined.inputs[0])
    nt.links.new(gdim.outputs[0], combined.inputs[1])
    em_line = nt.nodes.new("ShaderNodeEmission")
    em_line.inputs["Color"].default_value = CYAN2
    em_line.inputs["Strength"].default_value = 2.4
    # translucent navy film between the lines
    film = nt.nodes.new("ShaderNodeBsdfPrincipled")
    film.inputs["Base Color"].default_value = srgb("#10263a")
    film.inputs["Roughness"].default_value = 0.6
    try:
        film.inputs["Alpha"].default_value = 0.12
        film.inputs["Emission Color"].default_value = srgb("#15374f")
        film.inputs["Emission Strength"].default_value = 0.10
    except KeyError:
        pass
    mixs = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(combined.outputs[0], mixs.inputs["Fac"])
    nt.links.new(film.outputs["BSDF"], mixs.inputs[1])
    nt.links.new(em_line.outputs["Emission"], mixs.inputs[2])
    nt.links.new(mixs.outputs["Shader"], out.inputs["Surface"])
    mat.blend_method = "BLEND"
    return mat

NX, NY = 200, 130
X0, X1, Y0, Y1 = HX0, HX1, HY0, HY1
verts, faces = [], []
for j in range(NY + 1):
    y = Y0 + (Y1 - Y0) * j / NY
    for i in range(NX + 1):
        x = X0 + (X1 - X0) * i / NX
        verts.append((x, y, HOLO_Z + height(x, y)))
for j in range(NY):
    for i in range(NX):
        a = j * (NX + 1) + i
        faces.append((a, a + 1, a + NX + 2, a + NX + 1))
holo = make_mesh("holo_terrain", verts, faces, holo_material())

# hologram projector beams from the chip corners up to the terrain
M_PROJ = glow("proj", srgb("#1b3f52"), 0.6)
for (px, py) in [(-6.0, -1.4), (6.9, -1.4), (-6.0, 7.0), (6.9, 7.0)]:
    add_cyl((px, py, 0.05), 0.10, 0.10, plain("projbase", srgb("#182238"), 0.4, 0.6), name="projbase")
    tube_from_points("projbeam", [(px, py, 0.1), (px * 0.95, py * 0.95 + 0.2, HOLO_Z + 0.25)],
                     0.012, M_PROJ)

# ---------------------------------------------------------------- trajectory on the hologram
def hz_at(x, y):
    return HOLO_Z + height(x, y)

# lead-in: from the TO device's output on the chip up onto the hologram panel
lead_in = [(to_cx + 0.3, to_cy - 1.3, 0.12), (to_cx - 0.5, to_cy - 0.2, 0.35),
           (-5.6, -1.6, HOLO_Z + 0.15), (-5.3, -0.9, hz_at(-5.3, -0.9) + 0.05)]
tube_from_points("lead_in", lead_in, 0.020, glow("lead_in_m", GOLD, 3.0))

traj_pts = []
climb1 = [(-5.3, -0.9), (-4.6, -0.75), (-3.9, -0.6), (-3.3, -0.45), (-2.8, -0.3), (-2.4, -0.1)]
for x, y in climb1:
    traj_pts.append((x, y, hz_at(x, y) + 0.05))
for t in [i / 12 for i in range(1, 12)]:
    x = -2.4 + t * 2.8
    y = -0.1 + t * 0.5
    base = hz_at(-2.4, -0.1) * (1 - t) + hz_at(0.4, 0.4) * t
    traj_pts.append((x, y, base + 0.95 * math.sin(math.pi * t) + 0.08))
climb2 = [(0.4, 0.4), (1.0, 0.45), (1.6, 0.5), (2.05, 0.52)]
for x, y in climb2:
    traj_pts.append((x, y, hz_at(x, y) + 0.05))
tube_from_points("trajectory", traj_pts, 0.030, glow("traj_m", GOLD, 5.0))
M_ITER = plain("iter", ROSE, 0.3)
try:
    b = M_ITER.node_tree.nodes["Principled BSDF"]
    b.inputs["Emission Color"].default_value = ROSE
    b.inputs["Emission Strength"].default_value = 0.8
except KeyError:
    pass
for k, (x, y) in enumerate(climb1 + climb2):
    add_sphere((x, y, hz_at(x, y) + 0.09), 0.10, M_ITER, f"iter{k}")

# QA tunnel straight through the translucent local hill
qa_z = hz_at(-2.4, -0.1) - 0.45
tube_from_points("qa_tunnel", [(-4.1, -0.35, qa_z), (-1.05, -0.25, qa_z)], 0.038,
                 glow("qa_m", ROSE, 2.6))
bpy.ops.mesh.primitive_cone_add(radius1=0.085, depth=0.18,
                                location=(-0.95, -0.245, qa_z),
                                rotation=(0, math.radians(90), 0))
qa_tip = bpy.context.object
qa_tip.data.materials.append(glow("qa_tip_m", ROSE, 2.6))

# ---------------------------------------------------------------- flag at the global maximum
peak = (2.6, 0.6, hz_at(2.6, 0.6))
pole_h = 1.35
pole_x = peak[0] + 0.30
M_POLE = plain("pole", srgb("#3a4456"), 0.35, 0.6)
add_cyl((pole_x, peak[1], peak[2] + pole_h / 2 - 0.05), 0.024, pole_h, M_POLE, name="pole")
add_sphere((pole_x, peak[1], peak[2] + pole_h - 0.05), 0.04, M_POLE, name="pole_top")
fw, fh = 0.86, 0.46
fverts, ffaces = [], []
FN = 16
for j in range(2):
    for i in range(FN + 1):
        u = i / FN
        fverts.append((pole_x + 0.02 + u * fw,
                       peak[1] + 0.08 * math.sin(2.6 * u * math.pi) * (0.3 + 0.7 * u),
                       peak[2] + pole_h - 0.09 - j * fh - 0.05 * u))
for i in range(FN):
    ffaces.append((i, i + 1, FN + 2 + i, FN + 1 + i))
M_FLAG = plain("flag", srgb("#e8415f"), 0.55)
try:
    b = M_FLAG.node_tree.nodes["Principled BSDF"]
    b.inputs["Emission Color"].default_value = srgb("#e8415f")
    b.inputs["Emission Strength"].default_value = 0.5
except KeyError:
    pass
make_mesh("flag", fverts, ffaces, M_FLAG)
try:
    font_b = bpy.data.fonts.load("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
except Exception:
    font_b = None
tcurve = bpy.data.curves.new("flagtext", type="FONT")
tcurve.body = "∇f = 0"
if font_b:
    tcurve.font = font_b
tcurve.size = 0.19
tcurve.align_x = "CENTER"
tob = bpy.data.objects.new("flagtext", tcurve)
tob.location = (pole_x + 0.02 + fw / 2, peak[1] - 0.10, peak[2] + pole_h - 0.39)
tob.rotation_euler = (math.radians(90), 0, 0)
tob.data.materials.append(glow("flagtext_m", IVORY, 1.6))
tob.visible_shadow = False
scene.collection.objects.link(tob)

# ---------------------------------------------------------------- chibi 老師 (modeled on the dop.nycu.edu.tw portrait)
cx, cy = 2.14, 0.42
cz = hz_at(cx, cy)
M_SUIT = plain("suit", NAVY, 0.75)
M_HAIR = plain("hair", INK, 0.6)
M_SKIN = plain("skin", SKIN, 0.65)
try:
    b = M_SKIN.node_tree.nodes["Principled BSDF"]
    b.inputs["Subsurface Weight"].default_value = 0.25
    b.inputs["Subsurface Radius"].default_value = (0.05, 0.02, 0.015)
except KeyError:
    pass
M_IVORYP = plain("ivoryp", IVORY, 0.8)
M_TIE = plain("tie", TIE, 0.6)
try:
    b = M_TIE.node_tree.nodes["Principled BSDF"]
    b.inputs["Emission Color"].default_value = TIE
    b.inputs["Emission Strength"].default_value = 0.15
except KeyError:
    pass
M_INKP = plain("inkp", INK, 0.45)
M_MOUTH = plain("mouth", srgb("#8a4a4a"), 0.6)
M_BLUSH = plain("blush", srgb("#f28fa2"), 1.0)

# legs + shoes
add_capsule((cx - 0.085, cy, cz + 0.05), (cx - 0.085, cy, cz + 0.22), 0.048, M_SUIT, "legL")
add_capsule((cx + 0.085, cy, cz + 0.05), (cx + 0.085, cy, cz + 0.22), 0.048, M_SUIT, "legR")
add_sphere((cx - 0.085, cy - 0.025, cz + 0.035), 0.07, M_INKP, name="shoeL", scale=(1.0, 1.45, 0.62))
add_sphere((cx + 0.085, cy - 0.025, cz + 0.035), 0.07, M_INKP, name="shoeR", scale=(1.0, 1.45, 0.62))
# body
add_sphere((cx, cy, cz + 0.42), 0.21, M_SUIT, name="body", scale=(0.95, 0.82, 1.22))
add_sphere((cx, cy - 0.170, cz + 0.53), 0.055, M_IVORYP, name="shirt", scale=(0.9, 0.30, 1.15))
add_sphere((cx, cy - 0.185, cz + 0.455), 0.024, M_TIE, name="tie", scale=(0.9, 0.40, 2.3))
# arms: left raised cheer, right grips pole
shoulderL = (cx - 0.185, cy, cz + 0.585)
elbowL = (cx - 0.30, cy - 0.02, cz + 0.68)
handL = (cx - 0.345, cy - 0.03, cz + 0.82)
add_capsule(shoulderL, elbowL, 0.045, M_SUIT, "armL_upper")
add_capsule(elbowL, handL, 0.041, M_SUIT, "armL_fore")
add_sphere(handL, 0.058, M_SKIN, name="handL")
shoulderR = (cx + 0.185, cy, cz + 0.585)
elbowR = (cx + 0.32, cy + 0.02, cz + 0.64)
handR = (pole_x, peak[1], cz + 0.72)
add_capsule(shoulderR, elbowR, 0.045, M_SUIT, "armR_upper")
add_capsule(elbowR, handR, 0.041, M_SUIT, "armR_fore")
add_sphere(handR, 0.058, M_SKIN, name="handR")
# head
hz = cz + 0.98
add_sphere((cx, cy, hz), 0.295, M_SKIN, name="head")
# hair: cap + swept wispy bangs (per the portrait) + side pieces over the ears
add_sphere((cx, cy + 0.10, hz + 0.075), 0.302, M_HAIR, name="haircap", scale=(1.03, 1.0, 0.95))
bang_y = cy - 0.225
bangs = [
    # (x, z, rot_y_deg, len_scale, r)
    (-0.19, 0.150, 30, 1.05, 0.058),
    (-0.105, 0.180, 16, 1.15, 0.062),
    (0.0, 0.192, 3, 1.20, 0.064),
    (0.10, 0.180, -12, 1.15, 0.062),
    (0.185, 0.148, -28, 1.05, 0.058),
    (0.245, 0.108, -45, 0.95, 0.052),
]
for k, (bx_, bz_, rdeg, ls, br) in enumerate(bangs):
    add_sphere((cx + bx_, bang_y, hz + bz_), br, M_HAIR, name=f"bang{k}",
               scale=(0.70, 0.50, ls), rot=(0, math.radians(rdeg), 0))
add_sphere((cx - 0.275, cy + 0.02, hz - 0.02), 0.06, M_HAIR, name="sideL", scale=(0.55, 0.8, 1.7))
add_sphere((cx + 0.275, cy + 0.02, hz - 0.02), 0.06, M_HAIR, name="sideR", scale=(0.55, 0.8, 1.7))
# rectangular glasses (per the portrait): wide flat frames
for sgn in (-1, 1):
    bpy.ops.mesh.primitive_torus_add(major_radius=0.080, minor_radius=0.009,
                                     location=(cx + sgn * 0.115, cy - 0.283, hz + 0.015),
                                     rotation=(math.radians(90), 0, 0),
                                     major_segments=64, minor_segments=16)
    ob = bpy.context.object
    ob.scale = (1.28, 1.0, 0.68)
    ob.data.materials.append(M_INKP)
    bpy.ops.object.shade_smooth()
add_cyl((cx, cy - 0.296, hz + 0.03), 0.0072, 0.055, M_INKP, rot=(0, math.radians(90), 0), name="bridge")
for sgn in (-1, 1):
    add_capsule((cx + sgn * 0.215, cy - 0.262, hz + 0.02),
                (cx + sgn * 0.285, cy - 0.05, hz + 0.035), 0.0065, M_INKP, f"temple{sgn}")
# eyes + catchlight
M_CATCH = glow("catch", IVORY, 1.2)
for sgn in (-1, 1):
    add_sphere((cx + sgn * 0.113, cy - 0.278, hz + 0.006), 0.032, M_INKP, name=f"eye{sgn}")
    add_sphere((cx + sgn * 0.113 + 0.009, cy - 0.306, hz + 0.017), 0.006, M_CATCH, name=f"catch{sgn}")
# brows
for sgn in (-1, 1):
    add_capsule((cx + sgn * 0.152, cy - 0.270, hz + 0.102),
                (cx + sgn * 0.078, cy - 0.280, hz + 0.118), 0.0082, M_INKP, f"brow{sgn}")
# smile
smile_pts = [(cx - 0.055, cy - 0.284, hz - 0.117), (cx - 0.02, cy - 0.295, hz - 0.135),
             (cx + 0.02, cy - 0.295, hz - 0.135), (cx + 0.055, cy - 0.284, hz - 0.117)]
tube_from_points("smile", smile_pts, 0.010, M_MOUTH)
# blush
add_sphere((cx - 0.180, cy - 0.248, hz - 0.075), 0.040, M_BLUSH, name="blushL", scale=(0.85, 0.25, 0.5))
add_sphere((cx + 0.180, cy - 0.248, hz - 0.075), 0.040, M_BLUSH, name="blushR", scale=(0.85, 0.25, 0.5))

# ---------------------------------------------------------------- world, lights, haze
world = bpy.data.worlds.new("world")
scene.world = world
world.use_nodes = True
wnt = world.node_tree
bg = wnt.nodes["Background"]
grad = wnt.nodes.new("ShaderNodeTexGradient")
mapn = wnt.nodes.new("ShaderNodeMapping")
texco = wnt.nodes.new("ShaderNodeTexCoord")
mapn.inputs["Rotation"].default_value = (0, math.radians(-90), 0)
wnt.links.new(texco.outputs["Generated"], mapn.inputs["Vector"])
wnt.links.new(mapn.outputs["Vector"], grad.inputs["Vector"])
ramp = wnt.nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].position = 0.0
ramp.color_ramp.elements[0].color = srgb("#0d1626")   # horizon: deep blue glow
ramp.color_ramp.elements[1].position = 1.0
ramp.color_ramp.elements[1].color = srgb("#04060c")   # zenith: near black
wnt.links.new(grad.outputs["Fac"], ramp.inputs["Fac"])
wnt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
bg.inputs["Strength"].default_value = 1.0

# cool cyan rim from back-left
bpy.ops.object.light_add(type="AREA", location=(-9, 8, 5))
rimL = bpy.context.object
rimL.data.energy = 900
rimL.data.size = 9
rimL.data.color = (0.45, 0.85, 1.0)
rimL.rotation_euler = (math.radians(-55), 0, math.radians(-140))
# warm gold rim from back-right
bpy.ops.object.light_add(type="AREA", location=(9, 7, 4.5))
rimR = bpy.context.object
rimR.data.energy = 700
rimR.data.size = 8
rimR.data.color = (1.0, 0.78, 0.5)
rimR.rotation_euler = (math.radians(-58), 0, math.radians(140))
# soft front key so the character face reads
bpy.ops.object.light_add(type="AREA", location=(0.5, -9, 4.5))
key = bpy.context.object
key.data.energy = 260
key.data.size = 7
key.data.color = (0.95, 0.96, 1.0)
key.rotation_euler = (math.radians(58), 0, 0)

# warm fill dedicated to the character's face
bpy.ops.object.light_add(type="AREA", location=(1.4, -2.8, 5.6))
cfill = bpy.context.object
cfill.data.energy = 130
cfill.data.size = 3
cfill.data.color = (1.0, 0.9, 0.8)
cfill.rotation_euler = (math.radians(48), 0, math.radians(-8))

# gentle haze for neon glow
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 2.5, 2.2))
haze = bpy.context.object
haze.scale = (30, 22, 6)
hm = bpy.data.materials.new("haze")
hm.use_nodes = True
hnt = hm.node_tree
hnt.nodes.clear()
hout = hnt.nodes.new("ShaderNodeOutputMaterial")
vol = hnt.nodes.new("ShaderNodeVolumeScatter")
vol.inputs["Density"].default_value = 0.006
vol.inputs["Anisotropy"].default_value = 0.45
hnt.links.new(vol.outputs["Volume"], hout.inputs["Volume"])
haze.data.materials.append(hm)
haze.display_type = "WIRE"

# ---------------------------------------------------------------- camera
bpy.ops.object.camera_add(location=(0.0, -13.6, 6.0))
cam = bpy.context.object
scene.camera = cam
cam.data.lens = 40
cam.data.dof.use_dof = True
cam.data.dof.aperture_fstop = 3.5
target = bpy.data.objects.new("target", None)
target.location = (0.3, 1.0, 1.75)
scene.collection.objects.link(target)
tc = cam.constraints.new(type="TRACK_TO")
tc.target = target
tc.track_axis = "TRACK_NEGATIVE_Z"
tc.up_axis = "UP_Y"
cam.data.dof.focus_object = bpy.data.objects["head"]
if CLOSEUP:
    cam.location = (cx - 0.5, cy - 2.6, cz + 1.15)
    cam.data.lens = 80
    cam.data.dof.aperture_fstop = 8.0
    target.location = (cx + 0.15, cy, cz + 0.85)

# ---------------------------------------------------------------- render
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = 48 if PREVIEW else (128 if DRAFT else 320)
scene.cycles.use_denoising = True
scene.cycles.volume_bounces = 2
scene.render.resolution_x = 800 if PREVIEW else (1600 if DRAFT else 3200)
scene.render.resolution_y = 500 if PREVIEW else (1000 if DRAFT else 2000)
scene.render.filepath = OUT
scene.render.image_settings.file_format = "PNG"
try:
    scene.view_settings.view_transform = "Filmic"
    scene.view_settings.look = "Medium High Contrast"
except Exception:
    scene.view_settings.view_transform = "Standard"
scene.view_settings.exposure = 0.0

bpy.ops.render.render(write_still=True)
print("rendered ->", OUT)
