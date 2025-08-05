const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // Create shared library for Python FFI
    const lib = b.addSharedLibrary(.{
        .name = "pyfunc_zig",
        .root_source_file = b.path("math_ops.zig"),
        .target = target,
        .optimize = optimize,
    });

    // Install the library
    b.installArtifact(lib);

    // Create a step for building the library
    const build_step = b.step("lib", "Build the shared library");
    build_step.dependOn(&lib.step);
}
