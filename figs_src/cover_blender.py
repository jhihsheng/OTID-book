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


# ---------------------------------------------------------------- light beams: bright core + soft transparent halo
def halo_material(name, color, strength, transparency=0.72):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = color
    em.inputs["Strength"].default_value = strength
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mx = nt.nodes.new("ShaderNodeMixShader")
    mx.inputs["Fac"].default_value = 1.0 - transparency
    nt.links.new(tr.outputs["BSDF"], mx.inputs[1])
    nt.links.new(em.outputs["Emission"], mx.inputs[2])
    nt.links.new(mx.outputs["Shader"], out.inputs["Surface"])
    return mat

def beam(name, pts, color, core_r=0.009, halo_r=0.05, core_s=14.0, halo_s=1.2,
         core_color=None):
    """Nature-Photonics-style beam: razor core + inner glow + wide soft bloom."""
    core = tube_from_points(name + "_core", pts, core_r,
                            glow(name + "_core_m", core_color or IVORY, core_s))
    core.visible_shadow = False
    h1 = tube_from_points(name + "_h1", pts, halo_r,
                          halo_material(name + "_h1_m", color, halo_s, transparency=0.75))
    h1.visible_shadow = False
    h2 = tube_from_points(name + "_h2", pts, halo_r * 2.6,
                          halo_material(name + "_h2_m", color, halo_s * 0.30, transparency=0.90))
    h2.visible_shadow = False
    return core

def flash(name, loc, color, r=0.05, s=8.0):
    """Blooming impact point."""
    add_sphere(loc, r, glow(name + "_c", srgb("#fff3d0"), s), name=name)
    for rr, ss, tr in [(r * 2.4, s * 0.18, 0.78), (r * 5.0, s * 0.05, 0.92)]:
        ob = add_sphere(loc, rr, halo_material(f"{name}_{rr:.2f}", color, ss, transparency=tr),
                        name=name + "_h")
        ob.visible_shadow = False

def parent_group(before_names, name, loc, rot_deg, scl):
    """Parent every object created since `before_names` to a transformed empty."""
    emp = bpy.data.objects.new(name, None)
    scene.collection.objects.link(emp)
    emp.location = loc
    emp.rotation_euler = (math.radians(rot_deg[0]), math.radians(rot_deg[1]), math.radians(rot_deg[2]))
    emp.scale = (scl, scl, scl)
    for ob in list(bpy.data.objects):
        if ob.name in before_names or ob is emp:
            continue
        if ob.parent is None and ob.type in {"MESH", "CURVE"}:
            ob.parent = emp
    return emp

# ---------------------------------------------------------------- chip feature 1: TO waveguide bend (front-left)
# real-device look (cf. published TO polarization splitters): a pale silicon slab
# with organic void cutouts and a 90-degree bend channel; the routed field glows
# hot orange like a simulated intensity map
_before = set(o.name for o in bpy.data.objects)
# course-style bend (cf. 08_OTID_meep_adjoint): square design region whose
# optimized density forms a diagonal band; input waveguide left, output top
add_box((0, 0, 0.030), (1.40, 1.40, 0.030), plain("to_sub", srgb("#243654"), 0.45, 0.35), name="to_sub")
TO_HALF = 1.1
TO_N = 36
def to_density(u, v):
    """True where silicon sits: main diagonal band + faint side stripes + dither."""
    d = (v - u) / math.sqrt(2)               # signed distance to the main diagonal
    wob = 0.06 * math.sin(4.2 * (u + v) + 1.2) + 0.03 * math.sin(9.0 * (u - v))
    if abs(d + wob) < 0.26:
        return True
    if abs(d + wob - 0.62) < 0.085 and (u + v) > -0.8:
        return True
    if abs(d + wob + 0.62) < 0.085 and (u + v) < 0.8:
        return True
    return False
cell = 2 * TO_HALF / TO_N
pverts, pfaces = [], []
z0, z1 = 0.062, 0.118
for j in range(TO_N):
    for i in range(TO_N):
        u = -TO_HALF + (i + 0.5) * cell
        v = -TO_HALF + (j + 0.5) * cell
        if not to_density(u, v):
            continue
        x0, x1 = u - cell * 0.5, u + cell * 0.5
        y0_, y1_ = v - cell * 0.5, v + cell * 0.5
        b0 = len(pverts)
        pverts += [(x0, y0_, z0), (x1, y0_, z0), (x1, y1_, z0), (x0, y1_, z0),
                   (x0, y0_, z1), (x1, y0_, z1), (x1, y1_, z1), (x0, y1_, z1)]
        pfaces += [(b0, b0 + 1, b0 + 2, b0 + 3), (b0 + 4, b0 + 5, b0 + 6, b0 + 7),
                   (b0, b0 + 1, b0 + 5, b0 + 4), (b0 + 1, b0 + 2, b0 + 6, b0 + 5),
                   (b0 + 2, b0 + 3, b0 + 7, b0 + 6), (b0 + 3, b0, b0 + 4, b0 + 7)]
M_SI = plain("to_si", srgb("#7f95b5"), 0.4, 0.15)
to_mesh = bpy.data.meshes.new("to_pixels")
to_mesh.from_pydata(pverts, [], pfaces)
to_mesh.update()
to_ob = bpy.data.objects.new("to_pixels", to_mesh)
to_ob.data.materials.append(M_SI)
scene.collection.objects.link(to_ob)
# waveguide stubs: in from the left (v=-0.78), out at the top (u=+0.78)
add_box((-1.42, -0.78, 0.09), (0.35, 0.10, 0.028), M_SI, name="wg_in")
add_box((0.78, 1.42, 0.09), (0.10, 0.35, 0.028), M_SI, name="wg_out")
# cyan light routed along the diagonal
bend_pts = [(-1.85, -0.78, 0.135), (-1.05, -0.78, 0.135), (-0.45, -0.62, 0.14),
            (0.1, -0.15, 0.14), (0.55, 0.45, 0.14), (0.78, 1.05, 0.135), (0.78, 1.85, 0.135)]
beam("light_bend", bend_pts, CYAN2, core_r=0.018, halo_r=0.07,
     core_s=12.0, halo_s=1.5, core_color=srgb("#e8fbff"))
flash("bend_hot", (0.1, -0.15, 0.15), CYAN2, r=0.045, s=5.0)

parent_group(_before, "grp_to", (-7.5, 9.6, 0.1), (40, 0, 8), 1.1)

# ---------------------------------------------------------------- chip feature 2: 1D grating + diffraction (front-right)
_before = set(o.name for o in bpy.data.objects)
# 10-layer thin-film filter (labs/tmm mini-project): broadband light in, blue out
M_LO = plain("flt_lo", srgb("#cfd9ea"), 0.35, 0.1)
M_HI = plain("flt_hi", srgb("#33507a"), 0.3, 0.4)
for k in range(10):
    add_box((0, 0, 0.05 + k * 0.062), (0.62, 0.42, 0.026), M_LO if k % 2 == 0 else M_HI, name=f"flt{k}")
flt_top = 0.05 + 9 * 0.062 + 0.026
# broadband (warm-white) incidence onto the top face
beam("flt_in", [(-1.15, -0.35, flt_top + 2.0), (-0.12, -0.04, flt_top + 0.02)],
     srgb("#f2ead8"), core_r=0.013, halo_r=0.055, core_s=10.0, halo_s=1.1,
     core_color=srgb("#fffdf4"))
flash("flt_hit", (-0.1, -0.03, flt_top + 0.03), srgb("#f2ead8"), r=0.05, s=6.0)
# faint reflected remainder + strong transmitted blue
beam("flt_ref", [(-0.1, -0.03, flt_top + 0.02), (0.75, -0.28, flt_top + 1.15)],
     srgb("#e8d8c0"), core_r=0.005, halo_r=0.02, core_s=2.0, halo_s=0.3)
beam("flt_out", [(-0.1, -0.03, 0.05), (0.55, 0.2, -1.75)],
     srgb("#3f6dff"), core_r=0.013, halo_r=0.06, core_s=10.0, halo_s=1.5,
     core_color=srgb("#cfe0ff"))

parent_group(_before, "grp_filter", (6.8, 9.6, 1.9), (35, 0, -10), 1.3)

# ---------------------------------------------------------------- chip feature 3: binary-phase OPA
# the course QA mini-project: a 1D optical phased array with a 0/pi binary phase
# profile, its beams interfering into a steered main lobe toward the target
_before = set(o.name for o in bpy.data.objects)
add_box((0, 0, 0.045), (1.05, 0.42, 0.045), plain("opa_base", srgb("#182338"), 0.4, 0.5), name="opa_base")
PHASES = [0, 1, 0, 0, 1, 0, 1, 1]
M_PH0 = glow("ph0", GOLD, 2.2)
M_PH1 = glow("ph1", ROSE, 2.2)
conv = (0.55, 0.0, 1.7)
opa_target = (2.35, 0.0, 3.55)
for k, ph in enumerate(PHASES):
    ex = -0.79 + k * 0.225
    add_box((ex, 0, 0.115), (0.075, 0.11, 0.055), plain(f"em{k}", srgb("#2c3c5c"), 0.35, 0.5), name=f"em{k}")
    add_box((ex, 0, 0.155), (0.055, 0.08, 0.012), M_PH0 if ph == 0 else M_PH1, name=f"emt{k}")
    beam(f"opa_b{k}", [(ex, 0, 0.17), conv], srgb("#b28bff"),
         core_r=0.006, halo_r=0.026, core_s=6.0, halo_s=0.6)
# the rays merge into one steered main lobe (no burst at the crossing)
beam("opa_main", [(0.42, 0.0, 1.5), opa_target], srgb("#b28bff"), core_r=0.016, halo_r=0.07,
     core_s=15.0, halo_s=1.8, core_color=srgb("#efe6ff"))
import mathutils as _mu
_dirv = (_mu.Vector(opa_target) - _mu.Vector(conv)).normalized()
for frac, arc_r in [(0.40, 0.20), (0.62, 0.30), (0.82, 0.42)]:
    cen = _mu.Vector(conv) + (_mu.Vector(opa_target) - _mu.Vector(conv)) * frac
    side = _dirv.cross(_mu.Vector((0, -1, 0))).normalized()
    up2 = _dirv.cross(side).normalized()
    pts = []
    for a in [i / 10 for i in range(11)]:
        th = (a - 0.5) * 2.4
        pp = cen + side * (arc_r * math.sin(th)) + up2 * (arc_r * math.cos(th)) * 0.9
        pts.append((pp.x, pp.y, pp.z))
    arc = tube_from_points(f"wf_{frac}", pts, 0.008,
                           halo_material(f"wf_m_{frac}", srgb("#b28bff"), 1.6, transparency=0.55))
    arc.visible_shadow = False
# Ising spin row: the binary phase profile as up/down spins under the emitters
M_SUP = glow("spin_up_m", GOLD, 2.4)
M_SDN = glow("spin_dn_m", ROSE, 2.4)
for k, ph in enumerate(PHASES):
    ex = -0.79 + k * 0.225
    up = (ph == 0)
    mat = M_SUP if up else M_SDN
    z0s, z1s = (-0.62, -0.34) if up else (-0.34, -0.62)
    tube_from_points(f"spin_shaft{k}", [(ex, 0.0, z0s), (ex, 0.0, z1s)], 0.016, mat)
    bpy.ops.mesh.primitive_cone_add(radius1=0.05, depth=0.10,
                                    location=(ex, 0.0, z1s),
                                    rotation=(0, 0, 0) if up else (math.radians(180), 0, 0))
    tip = bpy.context.object
    tip.data.materials.append(mat)
parent_group(_before, "grp_opa", (0.0, 9.8, 0.55), (30, 0, -2), 1.2)

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
    # thermal height gradient
    zmap = nt.nodes.new("ShaderNodeMapRange")
    zmap.inputs["From Min"].default_value = HOLO_Z
    zmap.inputs["From Max"].default_value = HOLO_Z + 2.7
    nt.links.new(sep.outputs["Z"], zmap.inputs["Value"])
    zramp = nt.nodes.new("ShaderNodeValToRGB")
    zramp.color_ramp.elements[0].position = 0.0
    zramp.color_ramp.elements[0].color = srgb("#173a8a")
    zramp.color_ramp.elements[1].position = 1.0
    zramp.color_ramp.elements[1].color = srgb("#ff5d3a")
    for pos, col in [(0.30, "#00b4d8"), (0.52, "#3fd68a"), (0.72, "#ffd166"), (0.88, "#ff9b42")]:
        el = zramp.color_ramp.elements.new(pos)
        el.color = srgb(col)
    nt.links.new(zmap.outputs["Result"], zramp.inputs["Fac"])
    # translucent film with capped fresnel glow
    fres = nt.nodes.new("ShaderNodeLayerWeight")
    fres.inputs["Blend"].default_value = 0.35
    fstr = nt.nodes.new("ShaderNodeMapRange")
    fstr.inputs["From Min"].default_value = 0.0
    fstr.inputs["From Max"].default_value = 1.0
    fstr.inputs["To Min"].default_value = 0.4
    fstr.inputs["To Max"].default_value = 1.25
    nt.links.new(fres.outputs["Facing"], fstr.inputs["Value"])
    film_em = nt.nodes.new("ShaderNodeEmission")
    nt.links.new(zramp.outputs["Color"], film_em.inputs["Color"])
    nt.links.new(fstr.outputs["Result"], film_em.inputs["Strength"])
    tr1 = nt.nodes.new("ShaderNodeBsdfTransparent")
    film = nt.nodes.new("ShaderNodeMixShader")
    film.inputs["Fac"].default_value = 0.55
    nt.links.new(tr1.outputs["BSDF"], film.inputs[1])
    nt.links.new(film_em.outputs["Emission"], film.inputs[2])
    # thin translucent purple grid
    def gridband(axis_out):
        dv = nt.nodes.new("ShaderNodeMath"); dv.operation = "DIVIDE"
        dv.inputs[1].default_value = 0.8
        nt.links.new(axis_out, dv.inputs[0])
        fr2 = nt.nodes.new("ShaderNodeMath"); fr2.operation = "FRACT"
        nt.links.new(dv.outputs[0], fr2.inputs[0])
        lt2 = nt.nodes.new("ShaderNodeMath"); lt2.operation = "LESS_THAN"
        lt2.inputs[1].default_value = 0.020
        nt.links.new(fr2.outputs[0], lt2.inputs[0])
        return lt2
    gx = gridband(sep.outputs["X"])
    gy = gridband(sep.outputs["Y"])
    gmax = nt.nodes.new("ShaderNodeMath"); gmax.operation = "MAXIMUM"
    nt.links.new(gx.outputs[0], gmax.inputs[0])
    nt.links.new(gy.outputs[0], gmax.inputs[1])
    gscale = nt.nodes.new("ShaderNodeMath"); gscale.operation = "MULTIPLY"
    gscale.inputs[1].default_value = 0.85
    nt.links.new(gmax.outputs[0], gscale.inputs[0])
    grid_em = nt.nodes.new("ShaderNodeEmission")
    grid_em.inputs["Color"].default_value = srgb("#b78fe0")
    grid_em.inputs["Strength"].default_value = 2.0
    tr2 = nt.nodes.new("ShaderNodeBsdfTransparent")
    grid_sh = nt.nodes.new("ShaderNodeMixShader")
    grid_sh.inputs["Fac"].default_value = 0.65
    nt.links.new(tr2.outputs["BSDF"], grid_sh.inputs[1])
    nt.links.new(grid_em.outputs["Emission"], grid_sh.inputs[2])
    chain1 = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(gscale.outputs[0], chain1.inputs["Fac"])
    nt.links.new(film.outputs["Shader"], chain1.inputs[1])
    nt.links.new(grid_sh.outputs["Shader"], chain1.inputs[2])
    # light-blue contour lines with slope-compensated (constant screen) width
    nrm = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(geo.outputs["Normal"], nrm.inputs["Vector"])
    nz2 = nt.nodes.new("ShaderNodeMath"); nz2.operation = "MULTIPLY"
    nt.links.new(nrm.outputs["Z"], nz2.inputs[0])
    nt.links.new(nrm.outputs["Z"], nz2.inputs[1])
    one_m = nt.nodes.new("ShaderNodeMath"); one_m.operation = "SUBTRACT"
    one_m.inputs[0].default_value = 1.0
    nt.links.new(nz2.outputs[0], one_m.inputs[1])
    root = nt.nodes.new("ShaderNodeMath"); root.operation = "SQRT"
    nt.links.new(one_m.outputs[0], root.inputs[0])
    nzc = nt.nodes.new("ShaderNodeMath"); nzc.operation = "MAXIMUM"
    nzc.inputs[1].default_value = 0.2
    nt.links.new(nrm.outputs["Z"], nzc.inputs[0])
    tanv = nt.nodes.new("ShaderNodeMath"); tanv.operation = "DIVIDE"
    nt.links.new(root.outputs[0], tanv.inputs[0])
    nt.links.new(nzc.outputs[0], tanv.inputs[1])
    tmul = nt.nodes.new("ShaderNodeMath"); tmul.operation = "MULTIPLY"
    tmul.inputs[1].default_value = 0.10
    nt.links.new(tanv.outputs[0], tmul.inputs[0])
    tmin = nt.nodes.new("ShaderNodeMath"); tmin.operation = "MINIMUM"
    tmin.inputs[1].default_value = 0.15
    nt.links.new(tmul.outputs[0], tmin.inputs[0])
    thr = nt.nodes.new("ShaderNodeMath"); thr.operation = "MAXIMUM"
    thr.inputs[1].default_value = 0.014
    nt.links.new(tmin.outputs[0], thr.inputs[0])
    cmul = nt.nodes.new("ShaderNodeMath"); cmul.operation = "MULTIPLY"
    cmul.inputs[1].default_value = 6.0
    nt.links.new(sep.outputs["Z"], cmul.inputs[0])
    cfr = nt.nodes.new("ShaderNodeMath"); cfr.operation = "FRACT"
    nt.links.new(cmul.outputs[0], cfr.inputs[0])
    cmask = nt.nodes.new("ShaderNodeMath"); cmask.operation = "LESS_THAN"
    nt.links.new(cfr.outputs[0], cmask.inputs[0])
    nt.links.new(thr.outputs[0], cmask.inputs[1])
    cont_em = nt.nodes.new("ShaderNodeEmission")
    cont_em.inputs["Color"].default_value = srgb("#9fd0ee")
    cont_em.inputs["Strength"].default_value = 2.4
    tr3 = nt.nodes.new("ShaderNodeBsdfTransparent")
    cont_sh = nt.nodes.new("ShaderNodeMixShader")
    cont_sh.inputs["Fac"].default_value = 0.80
    nt.links.new(tr3.outputs["BSDF"], cont_sh.inputs[1])
    nt.links.new(cont_em.outputs["Emission"], cont_sh.inputs[2])
    chain2 = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(cmask.outputs[0], chain2.inputs["Fac"])
    nt.links.new(chain1.outputs["Shader"], chain2.inputs[1])
    nt.links.new(cont_sh.outputs["Shader"], chain2.inputs[2])
    # edge dissolve baked as a vertex attribute
    fattr = nt.nodes.new("ShaderNodeAttribute")
    fattr.attribute_name = "fade"
    tr4 = nt.nodes.new("ShaderNodeBsdfTransparent")
    final = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(fattr.outputs["Fac"], final.inputs["Fac"])
    nt.links.new(tr4.outputs["BSDF"], final.inputs[1])
    nt.links.new(chain2.outputs["Shader"], final.inputs[2])
    nt.links.new(final.outputs["Shader"], out.inputs["Surface"])
    return mat

def alpha_fade(x, y):
    """Wider dissolve band so the panel melts into space with no hard border."""
    def s(t):
        t = max(0.0, min(1.0, t))
        return t * t * (3 - 2 * t)
    return (s((x - HX0) / 2.4) * s((HX1 - x) / 2.4) *
            s((y - HY0) / 2.4) * s((HY1 - y) / 2.4))

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
fade_attr = holo.data.color_attributes.new(name="fade", type="FLOAT_COLOR", domain="POINT")
for _i, (_x, _y, _z) in enumerate(verts):
    _f = alpha_fade(_x, _y)
    fade_attr.data[_i].color = (_f, _f, _f, 1.0)

# ---------------------------------------------------------------- trajectory on the hologram
def hz_at(x, y):
    return HOLO_Z + height(x, y)

def add_cone_step(p, q, r, depth, mat, name):
    d = Vector(q) - Vector(p)
    mid = (Vector(p) + Vector(q)) / 2
    bpy.ops.mesh.primitive_cone_add(radius1=r, depth=depth, location=mid)
    ob = bpy.context.object
    ob.name = name
    ob.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
    ob.data.materials.append(mat)
    return ob

# --- steepest descent (gold): clean step-by-step ascent of the east flank
sd_xy = [(6.4, -1.1), (5.7, -0.7), (5.0, -0.35), (4.3, -0.02), (3.65, 0.25), (3.1, 0.45), (2.78, 0.56)]
sd_pts = [(x, y, hz_at(x, y) + 0.05) for x, y in sd_xy]
beam("sd_path", sd_pts, srgb("#43d97c"), core_r=0.012, halo_r=0.045, core_s=9.0,
     halo_s=1.1, core_color=srgb("#dfffe9"))
M_STEP = glow("sd_step", srgb("#b6f7c8"), 5.0)
for k in range(len(sd_pts) - 1):
    pa = (sd_xy[k][0], sd_xy[k][1], hz_at(*sd_xy[k]) + 0.07)
    pb = (sd_xy[k + 1][0], sd_xy[k + 1][1], hz_at(*sd_xy[k + 1]) + 0.07)
    mid = ((pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2, (pa[2] + pb[2]) / 2)
    add_cone_step(mid, pb, 0.065, 0.16, M_STEP, f"sd_step{k}")

# --- simulated annealing (light rose): wandering walk, then the hop over the saddle
sa_xy = [(-6.0, -1.3), (-5.3, -0.95), (-4.7, -1.15), (-4.1, -0.6), (-3.5, -0.85),
         (-3.0, -0.35), (-2.4, -0.1)]
sa_pts = [(x, y, hz_at(x, y) + 0.05) for x, y in sa_xy]
for t in [i / 12 for i in range(1, 12)]:
    x = -2.4 + t * 2.9
    y = -0.1 + t * 0.45
    base = hz_at(-2.4, -0.1) * (1 - t) + hz_at(0.5, 0.35) * t
    sa_pts.append((x, y, base + 0.95 * math.sin(math.pi * t) + 0.08))
for x, y in [(0.5, 0.35), (1.1, 0.42), (1.7, 0.5), (2.25, 0.57)]:
    sa_pts.append((x, y, hz_at(x, y) + 0.05))
SA_ROSE = srgb("#ff7060")
beam("sa_path", sa_pts, SA_ROSE, core_r=0.013, halo_r=0.045, core_s=9.0,
     halo_s=1.1, core_color=srgb("#ffe0da"))
M_SAPT = plain("sa_pt", SA_ROSE, 0.4)
try:
    b = M_SAPT.node_tree.nodes["Principled BSDF"]
    b.inputs["Emission Color"].default_value = SA_ROSE
    b.inputs["Emission Strength"].default_value = 1.6
except KeyError:
    pass
for k, (x, y) in enumerate(sa_xy):
    add_sphere((x, y, hz_at(x, y) + 0.08), 0.07, M_SAPT, f"sa_pt{k}")

# --- QA (blue): tunnelling straight from the local hill into the global hill
qa_z = hz_at(-2.4, -0.1) - 0.35
qa_a = (-2.75, -0.15, qa_z)
qa_b = (1.95, 0.42, qa_z)
beam("qa_beam", [qa_a, qa_b], srgb("#4a9eff"),
     core_r=0.012, halo_r=0.05, core_s=10.0, halo_s=1.2, core_color=srgb("#d6e8ff"))
_d = (Vector(qa_b) - Vector(qa_a)).normalized()
bpy.ops.mesh.primitive_cone_add(radius1=0.085, depth=0.18,
                                location=(qa_b[0] + _d.x * 0.09, qa_b[1] + _d.y * 0.09, qa_z))
qa_tip = bpy.context.object
qa_tip.rotation_euler = _d.to_track_quat("Z", "Y").to_euler()
qa_tip.data.materials.append(glow("qa_tip_m", srgb("#4a9eff"), 3.0))

# ---------------------------------------------------------------- global maximum marker
# (the anime-style 老師 figure and the ∇f = 0 flag are drawn as a 2D layer at
# compose time — see figs_src/cover_compose.py)
peak = (2.6, 0.6, hz_at(2.6, 0.6))
add_sphere((peak[0], peak[1], peak[2] + 0.10), 0.11, glow("opt_marker", IVORY, 6.0), name="opt_marker")
mark_h = add_sphere((peak[0], peak[1], peak[2] + 0.10), 0.22,
                    halo_material("opt_halo", IVORY, 1.0), name="opt_halo")
mark_h.visible_shadow = False

# ---------------------------------------------------------------- world, lights, haze
world = bpy.data.worlds.new("world")
scene.world = world
world.use_nodes = True
wnt = world.node_tree
bg = wnt.nodes["Background"]
texco = wnt.nodes.new("ShaderNodeTexCoord")
mapn = wnt.nodes.new("ShaderNodeMapping")
mapn.inputs["Rotation"].default_value = (0, math.radians(-90), 0)
wnt.links.new(texco.outputs["Generated"], mapn.inputs["Vector"])
# vertical base gradient: near-black with a faint indigo horizon
grad = wnt.nodes.new("ShaderNodeTexGradient")
wnt.links.new(mapn.outputs["Vector"], grad.inputs["Vector"])
base = wnt.nodes.new("ShaderNodeValToRGB")
base.color_ramp.elements[0].position = 0.0
base.color_ramp.elements[0].color = srgb("#0a0820")
base.color_ramp.elements[1].position = 1.0
base.color_ramp.elements[1].color = srgb("#030207")
wnt.links.new(grad.outputs["Fac"], base.inputs["Fac"])
# wispy nebula filaments (blue with purple/magenta accents)
neb_noise = wnt.nodes.new("ShaderNodeTexNoise")
neb_noise.inputs["Scale"].default_value = 1.15
neb_noise.inputs["Detail"].default_value = 8.0
neb_noise.inputs["Roughness"].default_value = 0.68
wnt.links.new(texco.outputs["Generated"], neb_noise.inputs["Vector"])
neb = wnt.nodes.new("ShaderNodeValToRGB")
neb.color_ramp.elements[0].position = 0.42
neb.color_ramp.elements[0].color = (0, 0, 0, 1)
neb.color_ramp.elements[1].position = 0.95
neb.color_ramp.elements[1].color = srgb("#5c3a78")
for pos, col in [(0.58, "#10173f"), (0.72, "#241a55"), (0.84, "#3d2a68")]:
    el = neb.color_ramp.elements.new(pos)
    el.color = srgb(col)
wnt.links.new(neb_noise.outputs["Fac"], neb.inputs["Fac"])
mix1 = wnt.nodes.new("ShaderNodeMixRGB"); mix1.blend_type = "ADD"
mix1.inputs["Fac"].default_value = 0.38
wnt.links.new(base.outputs["Color"], mix1.inputs[1])
wnt.links.new(neb.outputs["Color"], mix1.inputs[2])
# two-layer procedural starfield
def star_layer(scale, thresh, power, gain):
    vor = wnt.nodes.new("ShaderNodeTexVoronoi")
    vor.inputs["Scale"].default_value = scale
    vor.inputs["Randomness"].default_value = 1.0
    wnt.links.new(texco.outputs["Generated"], vor.inputs["Vector"])
    lt = wnt.nodes.new("ShaderNodeMath"); lt.operation = "LESS_THAN"
    lt.inputs[1].default_value = thresh
    wnt.links.new(vor.outputs["Distance"], lt.inputs[0])
    bw = wnt.nodes.new("ShaderNodeRGBToBW")
    wnt.links.new(vor.outputs["Color"], bw.inputs["Color"])
    pw = wnt.nodes.new("ShaderNodeMath"); pw.operation = "POWER"
    pw.inputs[1].default_value = power
    wnt.links.new(bw.outputs["Val"], pw.inputs[0])
    m1 = wnt.nodes.new("ShaderNodeMath"); m1.operation = "MULTIPLY"
    wnt.links.new(lt.outputs[0], m1.inputs[0])
    wnt.links.new(pw.outputs[0], m1.inputs[1])
    m2 = wnt.nodes.new("ShaderNodeMath"); m2.operation = "MULTIPLY"
    m2.inputs[1].default_value = gain
    wnt.links.new(m1.outputs[0], m2.inputs[0])
    return m2
s1 = star_layer(300.0, 0.09, 4.0, 16.0)   # dense faint stars
s2 = star_layer(90.0, 0.05, 6.0, 40.0)    # sparse bright stars
sadd = wnt.nodes.new("ShaderNodeMath"); sadd.operation = "ADD"
wnt.links.new(s1.outputs[0], sadd.inputs[0])
wnt.links.new(s2.outputs[0], sadd.inputs[1])
starcol = wnt.nodes.new("ShaderNodeMixRGB"); starcol.blend_type = "ADD"
wnt.links.new(sadd.outputs[0], starcol.inputs["Fac"])
wnt.links.new(mix1.outputs["Color"], starcol.inputs[1])
starcol.inputs[2].default_value = (0.92, 0.95, 1.0, 1.0)
wnt.links.new(starcol.outputs["Color"], bg.inputs["Color"])
bg.inputs["Strength"].default_value = 1.0

# cool cyan rim from back-left
bpy.ops.object.light_add(type="AREA", location=(-9, 8, 5))
rimL = bpy.context.object
rimL.data.energy = 900
rimL.data.size = 9
rimL.data.color = (0.45, 0.85, 1.0)
rimL.rotation_euler = (math.radians(-55), 0, math.radians(-140))
# magenta rim from back-right (graphene-reference duotone)
bpy.ops.object.light_add(type="AREA", location=(9, 7, 4.5))
rimR = bpy.context.object
rimR.data.energy = 750
rimR.data.size = 8
rimR.data.color = (0.85, 0.45, 1.0)
rimR.rotation_euler = (math.radians(-58), 0, math.radians(140))
# soft front key so the character face reads
bpy.ops.object.light_add(type="AREA", location=(0.5, -9, 4.5))
key = bpy.context.object
key.data.energy = 260
key.data.size = 7
key.data.color = (0.95, 0.96, 1.0)
key.rotation_euler = (math.radians(58), 0, 0)

# soft wash for the background exemplars
bpy.ops.object.light_add(type="AREA", location=(0, 3.5, 9))
bwash = bpy.context.object
bwash.data.energy = 380
bwash.data.size = 12
bwash.data.color = (0.85, 0.88, 1.0)
bwash.rotation_euler = (math.radians(-38), 0, 0)

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
vol.inputs["Density"].default_value = 0.009
vol.inputs["Anisotropy"].default_value = 0.5
hnt.links.new(vol.outputs["Volume"], hout.inputs["Volume"])
haze.data.materials.append(hm)
haze.display_type = "WIRE"

# ---------------------------------------------------------------- camera
bpy.ops.object.camera_add(location=(0.0, -13.0, 9.0))
cam = bpy.context.object
scene.camera = cam
cam.data.lens = 40
cam.data.dof.use_dof = True
cam.data.dof.aperture_fstop = 3.5
target = bpy.data.objects.new("target", None)
target.location = (0.3, 1.6, 2.4)
scene.collection.objects.link(target)
tc = cam.constraints.new(type="TRACK_TO")
tc.target = target
tc.track_axis = "TRACK_NEGATIVE_Z"
tc.up_axis = "UP_Y"
cam.data.dof.focus_object = bpy.data.objects["opt_marker"]
if CLOSEUP:
    cam.location = (peak[0] - 0.5, peak[1] - 3.2, peak[2] + 1.0)
    cam.data.lens = 80
    cam.data.dof.aperture_fstop = 8.0
    target.location = (peak[0], peak[1], peak[2] + 0.3)

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
