/* yices.exe: lanza yices_shim.py dentro de un Job que muere con este proceso. */
#include <windows.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char** argv) {
    char exe[MAX_PATH], dir[MAX_PATH], cmd[32768];
    GetModuleFileNameA(NULL, exe, MAX_PATH);
    strcpy(dir, exe);
    const char BS = 92, QU = 34; /* barra invertida y comillas */
    char* barra = strrchr(dir, BS); if (barra) *barra = 0;
    snprintf(cmd, sizeof cmd, "%cC:/Python314/python.exe%c -I %c%s/yices_shim.py%c", QU, QU, QU, dir, QU);
    for (int i = 1; i < argc; i++) {
        strncat(cmd, " \"", sizeof cmd - strlen(cmd) - 1);
        strncat(cmd, argv[i], sizeof cmd - strlen(cmd) - 1);
        strncat(cmd, "\"", sizeof cmd - strlen(cmd) - 1);
    }
    HANDLE job = CreateJobObjectA(NULL, NULL);
    JOBOBJECT_EXTENDED_LIMIT_INFORMATION info; ZeroMemory(&info, sizeof info);
    info.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE;
    SetInformationJobObject(job, JobObjectExtendedLimitInformation, &info, sizeof info);
    STARTUPINFOA si; PROCESS_INFORMATION pi;
    ZeroMemory(&si, sizeof si); si.cb = sizeof si;
    si.dwFlags = STARTF_USESTDHANDLES;
    si.hStdInput = GetStdHandle(STD_INPUT_HANDLE);
    si.hStdOutput = GetStdHandle(STD_OUTPUT_HANDLE);
    si.hStdError = GetStdHandle(STD_ERROR_HANDLE);
    if (!CreateProcessA(NULL, cmd, NULL, NULL, TRUE, CREATE_SUSPENDED, NULL, NULL, &si, &pi)) {
        printf("unknown\n"); return 0;
    }
    AssignProcessToJobObject(job, pi.hProcess);
    ResumeThread(pi.hThread);
    WaitForSingleObject(pi.hProcess, INFINITE);
    DWORD rc = 0; GetExitCodeProcess(pi.hProcess, &rc);
    return (int)rc;
}
