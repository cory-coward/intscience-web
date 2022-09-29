from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import MaintenanceLogForm, GardnerDenverLogForm
from .models import MaintenanceLog, GardnerDenverLog

from django.shortcuts import render
from plc_core.plc_measurements import PlcMeasurements


class MaintenanceLogListView(LoginRequiredMixin, ListView):
    model = MaintenanceLog
    queryset = MaintenanceLog.objects.order_by('-created_on')
    paginate_by = 20


class MaintenanceLogDetailView(LoginRequiredMixin, DetailView):
    model = MaintenanceLog


class MaintenanceLogCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = MaintenanceLog
    form_class = MaintenanceLogForm
    permission_required = ('maintenance_logs.add_maintenance_log', )
    permission_denied_message = 'You do not have sufficient privileges to add maintenance logs.'
    success_url = reverse_lazy('maintenance_logs:maintenance-logs')
    success_message = 'Maintenance log successfully added.'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(MaintenanceLogCreateView, self).form_valid(form)


class GardnerDenverLogListView(LoginRequiredMixin, ListView):
    model = GardnerDenverLog
    queryset = GardnerDenverLog.objects.order_by('-created_on')
    template_name = 'maintenance_logs/gardnerdenver_list.html'
    paginate_by = 20


class GardnerDenverLogDetailView(LoginRequiredMixin, DetailView):
    model = GardnerDenverLog
    template_name = 'maintenance_logs/gardnerdenver_detail.html'


class GardnerDenverLogCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = GardnerDenverLog
    form_class = GardnerDenverLogForm
    template_name = 'maintenance_logs/gardnerdenver_form.html'
    permission_required = ('maintenance_logs.add_gardner_denver_log',)
    permission_denied_message = 'You do not have sufficient privileges to add Gardner Denver logs.'
    success_url = reverse_lazy('maintenance_logs:gardner-denver-logs')
    success_message = 'Gardner Denver log successfully added.'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(GardnerDenverLogCreateView, self).form_valid(form)


def plc_test_view(request):
    PlcMeasurements.read_wells()
    return render(request, 'maintenance_logs/test.html', {})
