#include <iostream>
#include <format>
#include <cmath>
namespace ECR169B
{
    int t;
    int l, r;
    int L, R;
    int case_solver();
    void problem_solver();
} // namespace ECR169B
int main()
{
    // freopen("ECR169B.in", "r", stdin);

    ECR169B::problem_solver();

    // fclose(stdin);
    return 0;
}
namespace ECR169B
{
    int case_solver()
    {
        std::cin >> l >> r;
        std::cin >> L >> R;
        // std::cout << std::format("l={},r={};L={},R={}\n", l, r, L, R);
        /* main algorithm */
        if ((l > R) || (L > r))
        {
            return 1;
        }
        else
        {
            int le = std::max(l, L), ri = std::min(r, R);
            int ans = ri - le + 2;
            if (l == L)
            {
                ans--;
            }
            if (r == R)
            {
                ans--;
            }
            return ans;
        }
        return 114514;
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
} // namespace ECR169B
