#include <format>
#include <iostream>
#include <memory>
#include <algorithm>
#include <cmath>
namespace ECR169C
{
    int t;
    int n, k;
    std::shared_ptr<int[]> a;
    int case_solver();
    void problem_solver();
} // namespace ECR169C
int main()
{
    // freopen("ECR169C.in", "r", stdin);

    ECR169C::problem_solver();

    // fclose(stdin);
    return 0;
}
namespace ECR169C
{
    int case_solver()
    {
        /* INPUT */
        std::cin >> n >> k; // INPUT n,k
        a = std::make_shared<int[]>(n);
        for (size_t i = 0; i < n; i++)
        {
            std::cin >> a[i]; // INPUT a_i
        }
        /* main algorithm */
        std::sort(a.get(), a.get() + n, std::greater<int>());
        int len = n >> 1;
        bool is_odd = n & 1;
        int difference = 0;
        for (size_t i = 0; i < len; i++)
        {
            int tmp_alice = a[2 * i + 0];
            int tmp_bob = a[2 * i + 1];
            difference += tmp_alice - tmp_bob;
        }
        return std::max(0, difference - k) + is_odd * a[n - 1];
    }
    void problem_solver()
    {
        std::cin >> t;
        while (t--)
        {
            // std::cout << std::format("test case number == {:02d}\n", t);
            std::cout << std::format("{}\n", case_solver());
        }
    }
} // namespace ECR169C
