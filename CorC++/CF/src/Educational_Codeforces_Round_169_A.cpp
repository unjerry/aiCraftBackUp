#include <iostream>
#include <format>
#include <memory>
#include <string>
#include <cmath>
namespace ECR169A
{
    int t;
    int n;
    std::shared_ptr<int[]> x;

    std::string case_solver();
    void problem_solver();
} // namespace ECR169A
int main()
{
    // freopen("ECR169A.in", "r", stdin);

    ECR169A::problem_solver();

    // fclose(stdin);
    return 0;
}
namespace ECR169A
{
    std::string case_solver()
    {
        std::cin >> ECR169A::n; // n
        ECR169A::x = std::make_shared<int[]>(n);
        for (size_t i = 0; i < n; i++)
        {
            std::cin >> ECR169A::x[i]; // x_i
        }
        /* main algorithm */
        if (ECR169A::n != 2)
        {
            return "NO";
        }
        else
        {
            if (std::abs(x[0] - x[1]) <= 1)
            {
                return "NO";
            }
            else
            {
                return "YES";
            }
        }
        return "HELLO";
    }
    void problem_solver()
    {
        std::cin >> ECR169A::t;
        while (ECR169A::t--)
        {
            // std::cout << std::format("test case number == {:02d}\n", ECR169A::t);
            std::cout << std::format("{}\n", case_solver());
        }
    }
} // namespace ECR169A
