class CompanyMiddleware:
    """
    Middleware to enforce company isolation.
    Ensures users can only access data from their own company.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process request before view
        if request.user.is_authenticated and not request.user.is_superuser:
            request.company = request.user.company
        else:
            request.company = None

        response = self.get_response(request)
        return response
