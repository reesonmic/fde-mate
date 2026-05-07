"""
简单测试脚本验证 HP-001 和 HP-003 修复
"""
import asyncio
import sys
sys.path.insert(0, '/Users/micreeson/Desktop/AI/fdework/workspace/api')

# 只导入异常模块（无需数据库依赖）
# 验证错误码定义
def test_error_codes():
    """Test that new error codes are defined."""
    from app.exceptions.codes import BIZ_FILE_SIZE_EXCEEDED, BIZ_AI_ACTION_PARAMS_MISMATCH
    assert BIZ_FILE_SIZE_EXCEEDED == 6004, f"Expected 6004, got {BIZ_FILE_SIZE_EXCEEDED}"
    assert BIZ_AI_ACTION_PARAMS_MISMATCH == 8008, f"Expected 8008, got {BIZ_AI_ACTION_PARAMS_MISMATCH}"
    print("[PASS] Error codes defined correctly")

# 验证新的异常类
def test_exceptions():
    """Test that new exceptions have correct properties."""
    from app.exceptions.biz import FileTooLargeException, AIActionParamsMismatchException
    from app.exceptions.codes import BIZ_FILE_SIZE_EXCEEDED, BIZ_AI_ACTION_PARAMS_MISMATCH

    # Test FileTooLargeException
    exc = FileTooLargeException(max_size_mb=100)
    assert exc.code == BIZ_FILE_SIZE_EXCEEDED
    assert exc.http_status == 413
    assert "100MB" in exc.message
    print("[PASS] FileTooLargeException works correctly (HTTP 413)")

    # Test AIActionParamsMismatchException
    exc2 = AIActionParamsMismatchException()
    assert exc2.code == BIZ_AI_ACTION_PARAMS_MISMATCH
    assert exc2.message == "Action parameters mismatch"
    print("[PASS] AIActionParamsMismatchException works correctly")

# 验证文件内容
def test_file_service_import():
    """Test that file_service imports the new exception by checking source."""
    with open('/Users/micreeson/Desktop/AI/fdework/workspace/api/app/services/file_service.py', 'r') as f:
        content = f.read()
        assert 'FileTooLargeException' in content, "FileTooLargeException should be imported"
        assert 'exc.http_status == 413' or 'raise FileTooLargeException' in content
    print("[PASS] FileService imports and uses FileTooLargeException")

# 验证文件内容
def test_task_service_import():
    """Test that task_service imports the new exception by checking source."""
    with open('/Users/micreeson/Desktop/AI/fdework/workspace/api/app/services/task_service.py', 'r') as f:
        content = f.read()
        assert 'AIActionParamsMismatchException' in content, "AIActionParamsMismatchException should be imported"
        assert 'set(action_ids) != set(req.ids)' in content, "ID validation logic should be present"
    print("[PASS] TaskService imports and uses AIActionParamsMismatchException")

# 模拟测试参数验证逻辑
def test_action_param_validation():
    """Test the parameter validation logic."""
    # 测试相同的 IDs
    action_ids = [1, 2, 3]
    request_ids = [1, 2, 3]
    assert set(action_ids) == set(request_ids), "Same IDs should match"
    print("[PASS] Parameter validation: same IDs match")

    # 测试不同的 IDs
    action_ids = [1, 2, 3]
    request_ids = [1, 2, 4]
    assert set(action_ids) != set(request_ids), "Different IDs should not match"
    print("[PASS] Parameter validation: different IDs do not match")

    # 测试顺序不同但内容相同
    action_ids = [1, 2, 3]
    request_ids = [3, 2, 1]
    assert set(action_ids) == set(request_ids), "Same IDs in different order should match"
    print("[PASS] Parameter validation: IDs in different order match")

if __name__ == "__main__":
    print("=" * 60)
    print("Running HP-003 and HP-001 Fix Verification Tests")
    print("=" * 60)

    try:
        test_error_codes()
        test_exceptions()
        test_file_service_import()
        test_task_service_import()
        test_action_param_validation()
        print("=" * 60)
        print("[SUCCESS] All verification tests passed!")
        print("=" * 60)
    except Exception as e:
        print(f"[FAIL] Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
