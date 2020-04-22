
import argparse
import os
import subprocess

contrib_ops_path='onnxruntime/contrib_ops'
core_ops_path='onnxruntime/core/providers'
training_ops_path='orttraining/orttraining/training_ops'

contrib_ops_files = ['activation/activations_impl.cu',
                   'activation/activations_impl.h',
                   'activation/activations.cc',
                   'activation/activations.h',
                   'layer_norm_impl.cu',
                   'layer_norm_impl.h',
                   'layer_norm.cc',
                   'layer_norm.h'
]

core_ops_files = ['activation/activations_impl.cu',
                'activation/activations_impl.h',
                #'activation/activations.cc',
                'activation/activations.h',
                #'atomic/common.cuh',
                #'cu_inc/common.cuh',
                'cu_inc/unary_elementwise_impl.cuh',
                'math/clip_impl.cu',
                'math/clip_impl.h',
                'math/clip.cc',
                'math/clip.h',
                'math/softmax_impl.cu',
                'math/softmax_impl.cuh',
                'math/unary_elementwise_ops_impl.cu',
                'math/unary_elementwise_ops_impl.h',
                'math/unary_elementwise_ops.cc',
                'math/unary_elementwise_ops.h',
                'multi_tensor/common.cuh',
                #'reduction/reduction_functions.cu',
                #'reduction/reduction_functions.h',
                #'reduction/reduction_ops.cc',
                #'reduction/reduction_ops.h',
                'reduction/reduction_utils.cuh',
                'tensor/cast_op.cc',
                'tensor/cast_op.h',
                'tensor/concat_impl.cu',
                'tensor/concat_impl.h',
                'tensor/concat.cc',
                'tensor/concat.h',
                'tensor/gather_impl.cu',
                'tensor/gather_impl.h',
                'tensor/gather.cc',
                'tensor/gather.h',
                'tensor/identity_op.cc',
                'tensor/identity_op.h',
                'tensor/reshape.cc',
                'tensor/reshape.h',
                'tensor/shape_op.cc',
                'tensor/squeeze.cc',
                'tensor/squeeze.h',
                'tensor/unsqueeze.cc',
                'tensor/unsqueeze.h'
]

training_ops_files = ['activation/activations_grad_impl.cu',
                    'activation/activations_grad_impl.h',
                    'activation/activations_grad.cc',
                    'activation/activations_grad.h',
                    'communication/common.h',
                    'communication/recv.cc',
                    'communication/recv.h',
                    'communication/send.cc',
                    'communication/send.h',
                    'controlflow/group.cc',
                    'loss/softmaxcrossentropy_impl.cc',
                    'loss/softmaxcrossentropy_impl.cu',
                    'loss/softmaxcrossentropy_impl.h',
                    'math/isfinite.cc',
                    'math/isfinite.cu',
                    'math/isfinite.cuh',
                    'math/isfinite.h',
                    'math/mixed_precision_scale.cc',
                    'math/mixed_precision_scale.cu',
                    'math/mixed_precision_scale.h',
                    'math/softmax_grad_impl.cu',
                    'math/softmax_grad.cc',
                    'math/softmax_grad.h',
                    'math/transpose_matmul.cc',
                    'nn/dropout_impl.cu',
                    'nn/dropout_impl.h',
                    'nn/dropout.cc',
                    'nn/dropout.h',
                    'nn/layer_norm_impl.cu',
                    'nn/layer_norm_impl.h',
                    'nn/layer_norm.cc',
                    'nn/layer_norm.h',
                    'nn/trainable_dropout.cc',
                    'optimizer/adam.cc',
                    'optimizer/adam.cu',
                    'optimizer/adam.h',
                    'optimizer/common.cuh',
                    'optimizer/common.h',
                    'optimizer/gradient_control.cc',
                    'optimizer/gradient_control.cu',
                    'optimizer/gradient_control.h',
                    'optimizer/lamb.cc',
                    'optimizer/lamb.cu',
                    'optimizer/lamb.h',
                    'optimizer/sg.cc',
                    'optimizer/sg.cu',
                    'optimizer/sg.h',
                    'reduction/all.cc',
                    'reduction/all.cu',
                    'reduction/all.h',
                    'reduction/reduction_all.cc',
                    'reduction/reduction_all.cu',
                    'reduction/reduction_all.h',
                    'tensor/gather_grad_impl.cu',
                    'tensor/gather_grad_impl.h',
                    'tensor/gather_grad.cc',
                    'tensor/gather_grad.h',
                    'tensor/gather_nd_impl.cu',
                    'tensor/gather_nd_impl.h',
                    'tensor/gather_nd.cc',
                    'tensor/gather_nd.h',
                    'tensor/slice_grad.cc',
                    'tensor/slice_grad.h',
                    'tensor/view.cc',
                    'tensor/view.h'
]


HIPIFY_PERL='/opt/rocm/bin/hipify-perl'
FINDCODE='/opt/rocm/bin/findcode.sh'

def main():
    cuda_path = core_ops_path + '/cuda/'
    hip_path = core_ops_path + '/hip/'
    for file in core_ops_files:
        src_file_path = cuda_path + file
        dst_file_path = hip_path + file
        dir_name = os.path.dirname(dst_file_path)
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        with open(dst_file_path, 'w') as f:
            subprocess.run([HIPIFY_PERL, src_file_path], stdout=f)
        with open(dst_file_path) as f:
            s = f.read().replace('cuda', 'hip')
            s = s.replace('kCudaExecutionProvider', 'kHipExecutionProvider')
            s = s.replace('CudaAsyncBuffer', 'HipAsyncBuffer')
            s = s.replace('CudaKernel', 'HipKernel')
            s = s.replace('ToCudaType', 'ToHipType')
            s = s.replace('CudaT', 'HipT')
            s = s.replace('CUDA_LONG', 'HIP_LONG')
            s = s.replace('CUDA_RETURN_IF_ERROR', 'HIP_RETURN_IF_ERROR')
        with open(dst_file_path, 'w') as f:
            f.write(s)

if __name__ == '__main__':
    main()