from rest_framework.generics import CreateAPIView


class PaymentCreateView(CreateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
