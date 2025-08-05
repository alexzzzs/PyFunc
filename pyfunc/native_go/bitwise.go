package main

import (
	"C"
	"unsafe"
)

//export bitwise_and_go
func bitwise_and_go(data *C.int, size C.int, operand C.int) {
	for i := 0; i < int(size); i++ {
		*(*C.int)(unsafe.Pointer(uintptr(unsafe.Pointer(data)) + uintptr(i)*unsafe.Sizeof(*data))) &= operand
	}
}

//export bitwise_or_go
func bitwise_or_go(data *C.int, size C.int, operand C.int) {
	for i := 0; i < int(size); i++ {
		*(*C.int)(unsafe.Pointer(uintptr(unsafe.Pointer(data)) + uintptr(i)*unsafe.Sizeof(*data))) |= operand
	}
}

//export bitwise_xor_go
func bitwise_xor_go(data *C.int, size C.int, operand C.int) {
	for i := 0; i < int(size); i++ {
		*(*C.int)(unsafe.Pointer(uintptr(unsafe.Pointer(data)) + uintptr(i)*unsafe.Sizeof(*data))) ^= operand
	}
}

//export bitwise_not_go
func bitwise_not_go(data *C.int, size C.int) {
	for i := 0; i < int(size); i++ {
		*(*C.int)(unsafe.Pointer(uintptr(unsafe.Pointer(data)) + uintptr(i)*unsafe.Sizeof(*data))) = ^(*(*C.int)(unsafe.Pointer(uintptr(unsafe.Pointer(data)) + uintptr(i)*unsafe.Sizeof(*data))))
	}
}

//export left_shift_go
func left_shift_go(data *C.int, size C.int, bits C.int) {
	for i := 0; i < int(size); i++ {
		*(*C.int)(unsafe.Pointer(uintptr(unsafe.Pointer(data)) + uintptr(i)*unsafe.Sizeof(*data))) <<= bits
	}
}

//export right_shift_go
func right_shift_go(data *C.int, size C.int, bits C.int) {
	for i := 0; i < int(size); i++ {
		*(*C.int)(unsafe.Pointer(uintptr(unsafe.Pointer(data)) + uintptr(i)*unsafe.Sizeof(*data))) >>= bits
	}
}

func main() {}
